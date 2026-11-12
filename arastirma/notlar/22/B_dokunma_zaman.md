# B: Touch-based timeline, drawing and layout research notes

Date: 2026-11-12
Labels: [D] official or normative doc (MDN, W3C WCAG, MDN-hosted specs), [B] full text read by fetch, [O] search summary only (secondary, unverified), ERISILEMEDI = host or page not reachable, BULUNAMADI = not found.
Access notes:
- WebFetch failed with DNS errors (ENOTFOUND) for developer.mozilla.org, www.w3.org and www.lukew.com. curl through the proxy worked for these hosts, so text was extracted with trafilatura (run with python3 -I).
- developer.apple.com HIG pages return only a JavaScript shell via curl. Apple HIG body text is therefore ERISILEMEDI in this session.
- www.uxmatters.com (Hoober 2013 article) did not resolve via curl (redirect target www.uxmatters.com failed DNS). Hoober figures below are [O].
- MDN dvh/WebCodecs slugs returned 404 and were replaced by the MDN length and VideoDecoder pages.

---

## 1. Drawing with a finger (mask fix, region marking, brush)

- Pointer Events are one input model for mouse, touch and pen. [D] MDN "Pointer events" (https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events): pointer events add "pressure, contact geometry, tilt, etc." properties on top of mouse event properties.
- Pressure: "normalized pressure ... in the range of 0 to 1, where 0 and 1 represent the minimum and maximum pressure the hardware is capable of detecting". [D] MDN Pointer events property list.
- pointerrawupdate: a separate, high-frequency event, attached with el.onpointerrawupdate. [D] MDN Pointer events.
- getCoalescedEvents(): "returns a sequence of PointerEvent instances that were coalesced (merged) into a single pointermove or pointerrawupdate event". Its use: "Un-coalesced position changes are desirable in drawing applications". [D] MDN PointerEvent.getCoalescedEvents (https://developer.mozilla.org/en-US/docs/Web/API/PointerEvent/getCoalescedEvents). MDN compatibility box: "Limited availability", not Baseline.
- getPredictedEvents(): estimated future positions "based on past points, current velocity, and trajectory". Apps "can use the predicted events to 'draw ahead'... which may reduce perceived latency". Prediction is user-agent dependent. [D] MDN PointerEvent.getPredictedEvents (https://developer.mozilla.org/en-US/docs/Web/API/PointerEvent/getPredictedEvents). Compatibility: Baseline 2024, "Newly available".
- touch-action: [D] MDN touch-action (https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action), fetched via curl. Keywords: none, manipulation, pan-x, pan-y, pinch-zoom, auto. Setting none on the drawing surface stops browser pan and zoom so the page receives the pointer stream.
- Two-finger zoom vs one-finger drawing: [D] touch-action keywords show pinch-zoom is a separate keyword from pan-x/pan-y. Design inference (not a source claim): with touch-action: none on the canvas, the browser pinch is also disabled, so pinch must be implemented in app code by tracking two active pointerIds. Keep touch-action: none only on the canvas, not on the page.
- Touch Events (legacy) [D] MDN Touch events (https://developer.mozilla.org/en-US/docs/Web/API/Touch_events): browsers send emulated mouse events for single touch, and multi-touch "will usually only generate touch events". preventDefault() on the touch event suppresses emulated mouse events. Pointer Events are preferred over Touch Events for new code.
- iOS Safari: [O] WebKit Bugzilla 133180 and a 2019 WebKit comment say pointer events are "supported for the most part in Safari 13 onwards". [O] A 2018 Stack Overflow report says touch-action: none on canvas did not stop scrolling on iOS after iOS 11.3, and an answer adds that preventDefault "will do half of the trick". Unverified for current Safari; test on device.
- Apple Pencil: [O] Safari exposes pen input as pointerType "pen" with pressure, tiltX, tiltY. A secondary post warns pressure can read 0 for some input, so a fallback is needed. Same post says Pencil pressure is sampled at 240 Hz (not verified against Apple). [O] WebKit bug asks Safari to expose twist (Pencil Pro), current state unconfirmed.
- Palm rejection: BULUNAMADI as an official mechanism for Safari. [O] An Apple developer forum thread asks Safari/WKWebView to ignore touch while the pen is active; it is a request, not a feature.
- tilt standardization: [O] W3C Pointer Events Level 3 work adds altitudeAngle and azimuthAngle alongside tiltX/tiltY (secondary summary; spec at https://www.w3.org/TR/pointerevents/ not fetched in this session).

## 2. Canvas drawing performance

- [D] MDN "Optimizing canvas" (https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas), fetched via curl:
  - Pre-render repeated primitives on an offscreen canvas, then draw that onto the visible canvas.
  - "Avoid floating-point coordinates and use integers instead."
  - Cache scaled image sizes on an offscreen canvas instead of scaling in drawImage().
  - If there is no transparent backdrop: getContext("2d", { alpha: false }).
  - "With animations, use Window.requestAnimationFrame() instead of setInterval()."
  - Compare clearing methods (clearRect, fillRect, resizing the canvas).
- [D] MDN Window.requestAnimationFrame (https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame): callback receives a DOMHighResTimeStamp; the common pattern is one drawing pass per frame, scheduling the next with requestAnimationFrame(step).
- [D] MDN Window.devicePixelRatio (https://developer.mozilla.org/en-US/docs/Web/API/Window/devicePixelRatio): "ratio of the resolution in physical pixels to the resolution in CSS pixels". Page zoom changes it. Recipe for sharp canvas: set canvas.width = cssWidth * dpr, canvas.height = cssHeight * dpr, and CSS width/height to cssWidth/cssHeight, then scale the context by dpr.
- [D] MDN OffscreenCanvas (https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas): "available in Web Workers"; transferControlToOffscreen() on an HTMLCanvasElement moves rendering to a worker (example: main.js calls transferControlToOffscreen, then postMessage with [offscreen] as transfer list). requestAnimationFrame is usable in workers.
- [D] MDN ImageBitmap (https://developer.mozilla.org/en-US/docs/Web/API/ImageBitmap): "can be drawn to a <canvas> without undue latency", created with createImageBitmap(); has close() to release memory. This is the basis for pre-decoded frame caches (see section 3).
- [D] MDN VideoDecoder (https://developer.mozilla.org/en-US/docs/Web/API/VideoDecoder) is part of WebCodecs; it "decodes chunks of video" and exposes decodeQueueSize. Usable as an alternative to a hidden <video> seek loop when frame-accurate access is needed. Not verified: browser support status and iOS behaviour. WebCodecs main page at MDN returned a JS-only shell in this session.

## 3. Timeline scrubber design

- Native range input: [D] MDN input type=range (https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/range). min, max, step; "the granularity is 1" by default; setting step="1" on an integer index is the right choice for frame selection. Fallback: if not supported, it becomes a text input (not relevant for modern browsers).
- Fine adjustment: a native range can have a large hit area but at 1 px per step it may need a step of 1 over a large index range, so a slider with 1 px per frame on phones is hard to hit. Option: use step=1 and map a large track to frames, or add +/- buttons (button hit areas per section 5). This is a design inference.
- Touch target sizes:
  - [B] WCAG 2.2 SC 2.5.8 Target Size (Minimum), fetched via curl (https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html): "The size of the target for pointer inputs is at least 24 by 24 CSS pixels", with exceptions for spacing, equivalent controls, inline targets and user-agent controls. Note from same page: "the larger 44 by 44 CSS pixel measure" is the threshold of 2.5.5 (Enhanced).
  - [O] Apple HIG: 44 x 44 pt minimum for iOS and iPadOS controls; one source cites 8 pt spacing between targets (only one source; unverified). Apple HIG pages could not be read here (ERISILEMEDI for primary text).
  - [O] Material Design: 48 x 48 dp; padding can extend the hit area beyond the visible icon. Source: Google accessibility help "Touch target size" (https://support.google.com/accessibility/android/answer/7101858) was listed in search, not fetched.
- Frame selection: a scrubber that maps a continuous x to a frame index, with tap-to-jump and a value readout. Value text: [D] MDN aria-valuetext (https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-valuetext): "defines the human-readable text alternative of aria-valuenow for a range widget", e.g. "2024 March" instead of "3".
- Preloading and instant response: ImageBitmap cache plus offscreen canvas (see sections 2 and 3). Keep decoded bitmaps for a window around the current index (for example +/- N frames) and close() bitmaps that fall out of the window. Memory budget: not researched in this session (BULUNAMADI for a source with numbers).
- Smoothness target 30 to 60 frames per second: [D] requestAnimationFrame guide supports per-frame drawing; the specific 30/60 fps targets are a design target, not sourced.

## 4. One screen: map, timeline and small multiples (layout)

- Viewport units: [D] MDN CSS length (https://developer.mozilla.org/en-US/docs/Web/CSS/length) describes dynamic viewport units. "The dynamic viewport unit is represented by the dv prefix" and "dvh" equivalents; plain vh equals lvh (large viewport). The page notes that dynamic units can cause content to resize while scrolling. Recommended: use dvh for full-height bottom layouts, or 100% of a container set with JS-free fixed positioning.
- Safe areas: [D] MDN env() (https://developer.mozilla.org/en-US/docs/Web/CSS/env): env(safe-area-inset-top|right|bottom|left) is "the safe distance ... without risking it being cut off by the shape of a non-rectangular display". Use with a fallback: env(safe-area-inset-bottom, 0px). Baseline widely available.
- Viewport meta and a no-scroll layout are not researched further here.
- Bottom sheet pattern: [O] only, not fetched. Material 3 bottom-sheet page was fetched via curl but the extracted text was a JS-only shell (ERISILEMEDI). No source collected with a verified snap-point rule.
- Thumb zone: [O] Hoober 2013 observational study (UXmatters, "How Do Users Really Hold Mobile Devices?", Feb 2013). Search summary: 1,333 observations of people in public places; 780 people touching screens; about 49% one-handed, 36% cradling, 15% two-handed; right thumb 67% of one-handed users. The thumb-reach heat map is not part of the study's percentages (summary says the thumb zone diagrams come from later work). One blog's "75% of interactions" figure: no primary source found, treat as unverified.
  - ERISILEMEDI for the primary article text (www host failed DNS).
- Design implication (inference): keep the most-used controls (scrubber, play, sheet handle) in the bottom third of the screen, map in the upper area, comparison panels collapsible.

## 5. Accessibility

- Contrast: [B] WCAG 2.2 SC 1.4.3 Contrast (Minimum), fetched (https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): "contrast ratio of at least 4.5:1", large text at least 3:1. Rationale text: 3:1 "is the minimum level recommended by ISO-9241-3 and ANSI-HFES-100-1988".
  - [B-partial] SC 1.4.11 Non-text Contrast page was fetched (https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html); the 3:1 requirement for UI components and graphical objects was not extracted verbatim in this session. Treat as to-verify for scrubber thumb, map markers and region outlines.
- Reduced motion: [D] MDN prefers-reduced-motion (https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion): "@media (prefers-reduced-motion: reduce)" detects a user preference to "remove, reduce, or replace motion-based animations". Applies to any auto-play of the timeline. Also available as Sec-CH-Prefers-Reduced-Motion client hint (MDN).
- Screen reader and range: native <input type="range"> exposes its value; use aria-valuetext for a human label (MDN, see section 3). Keyboard: native range handles arrow keys; no source fetched on keyboard step behaviour for a custom canvas scrubber (BULUNAMADI).
- Touch alternatives to drawing: a canvas drawing surface is not reachable to a screen reader. Provide a non-drawing alternative (for example, select a region from a list or buttons). Source: not fetched; design inference.

---

## Open issues / gaps
1. Apple HIG text (44 pt, 8 pt spacing, safe areas, Pencil guidelines) not readable: developer.apple.com needs JavaScript. Needs a browser-rendered fetch or the built-in browser tool.
2. Current iOS Safari behaviour for touch-action: none + pinch and for palm rejection: only 2018/2019 secondary reports. Needs a device test.
3. Apple Pencil in Safari: pressure, tiltX and pointerType "pen" only from a secondary post. Verify on iPad with a Pencil.
4. Hoober 2013 figures: from search summary only (UXmatters host failed DNS). Primary text not verified.
5. Bottom sheet snap rules, Material 3 touch target page: not verified.
6. WebCodecs browser support on iOS: not verified (MDN WebCodecs page was JS-only).
7. Memory budget for ImageBitmap caches: no source found.
8. The network-level DNS failures (developer.mozilla.org, www.w3.org, www.lukew.com in WebFetch) are resolved by the curl route only. Attach these domains in session network settings to use WebFetch directly.
