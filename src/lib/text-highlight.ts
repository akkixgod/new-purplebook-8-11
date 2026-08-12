/** Bluebook-style passage highlighting with nested / overlapping layers. */

export const HL_CLASS = "sat-hl";
export const MAX_HL_LAYER = 3;

function isHighlightMark(el: Element | null): el is HTMLElement {
  return !!el && el.tagName === "MARK" && el.classList.contains(HL_CLASS);
}

/** How many sat-hl ancestors wrap this node (0 = none). */
export function highlightDepth(node: Node): number {
  let depth = 0;
  let el = node.parentElement;
  while (el) {
    if (isHighlightMark(el)) depth++;
    el = el.parentElement;
  }
  return depth;
}

function createHighlightMark(layer: number): HTMLMarkElement {
  const mark = document.createElement("mark");
  const clamped = Math.min(Math.max(layer, 1), MAX_HL_LAYER);
  mark.className = HL_CLASS;
  mark.dataset.layer = String(clamped);
  return mark;
}

/**
 * Text-node slices intersecting `range` under `root`.
 * Safe across existing <mark> boundaries (unlike Range#surroundContents).
 */
function textSlicesInRange(
  root: HTMLElement,
  range: Range
): { node: Text; start: number; end: number }[] {
  const slices: { node: Text; start: number; end: number }[] = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);

  let current: Node | null = walker.nextNode();
  while (current) {
    const text = current as Text;
    current = walker.nextNode();

    if (!text.length) continue;

    let intersects = false;
    try {
      intersects = range.intersectsNode(text);
    } catch {
      intersects = false;
    }
    if (!intersects) continue;

    let start = 0;
    let end = text.length;
    if (range.startContainer === text) start = range.startOffset;
    if (range.endContainer === text) end = range.endOffset;

    start = Math.max(0, Math.min(start, text.length));
    end = Math.max(0, Math.min(end, text.length));
    if (start < end) slices.push({ node: text, start, end });
  }

  return slices;
}

/**
 * Wrap a portion of a text node in a highlight mark.
 * Nesting inside an existing mark creates a double-highlight layer.
 */
function wrapTextSlice(node: Text, start: number, end: number): HTMLMarkElement | null {
  if (start >= end || !node.parentNode) return null;

  const depth = highlightDepth(node);
  if (depth >= MAX_HL_LAYER) return null;

  let mid: Text = node;
  if (start > 0) {
    mid = node.splitText(start);
    end -= start;
  }
  if (end < mid.length) {
    mid.splitText(end);
  }

  const mark = createHighlightMark(depth + 1);
  mid.parentNode!.insertBefore(mark, mid);
  mark.appendChild(mid);
  return mark;
}

/**
 * Apply a highlight over `range` inside the passage `root`.
 * Supports overlapping / nested highlights for double-highlight visuals.
 * Returns true if any text was wrapped.
 */
export function applyTextHighlight(root: HTMLElement, range: Range): boolean {
  if (range.collapsed) return false;

  const ancestor = range.commonAncestorContainer;
  if (ancestor !== root && !root.contains(ancestor)) return false;

  const slices = textSlicesInRange(root, range);
  if (slices.length === 0) return false;

  // Wrap from the end so earlier splits don't invalidate later node references.
  let applied = false;
  for (let i = slices.length - 1; i >= 0; i--) {
    const { node, start, end } = slices[i];
    if (!node.isConnected || !root.contains(node)) continue;
    if (wrapTextSlice(node, start, end)) applied = true;
  }

  return applied;
}
