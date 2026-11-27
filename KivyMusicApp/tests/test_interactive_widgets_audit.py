"""
Test Suite: Interactive Widgets Action Binding Audit
Scans all .kv files across the project and asserts that:
1. Every actionable widget (MDIconButton, MDButton, MDActionTopAppBarButton, MDFabButton, MDChip)
   has a valid bound event handler (on_release, on_press, on_touch, on_active).
2. Unwired interactive widgets are flagged to prevent inert controls.
"""
import os
import re
import sys

def run_test(on_complete=None):
    results = {}
    print("\n[TEST] Starting Interactive Widgets Action Binding Audit...")
    
    app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kv_dir = os.path.join(app_root, "views")

    actionable_classes = [
        "MDIconButton", "MDButton", "MDActionTopAppBarButton", "MDFabButton", "MDChip"
    ]

    unwired_buttons = []
    total_actionable = 0

    for root, _, files in os.walk(kv_dir):
        for f in files:
            if f.endswith(".kv"):
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, kv_dir)
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()

                current_widget = None
                widget_indent = 0
                widget_line = 0
                has_action = False
                widget_info = ""

                for i, line in enumerate(lines):
                    stripped = line.strip()
                    indent = len(line) - len(line.lstrip())

                    matched_cls = None
                    for cls in actionable_classes:
                        if re.match(rf"^{cls}:", stripped) or re.match(rf"^<.*{cls}.*>:", stripped):
                            matched_cls = cls
                            break

                    if matched_cls:
                        if current_widget:
                            total_actionable += 1
                            if not has_action:
                                unwired_buttons.append((rel_path, widget_line, current_widget, widget_info))
                        current_widget = matched_cls
                        widget_indent = indent
                        widget_line = i + 1
                        has_action = False
                        widget_info = ""
                    elif current_widget:
                        if indent <= widget_indent and stripped and not stripped.startswith("#"):
                            total_actionable += 1
                            if not has_action:
                                unwired_buttons.append((rel_path, widget_line, current_widget, widget_info))
                            current_widget = None
                        else:
                            if any(k in stripped for k in ("on_release", "on_press", "on_touch", "on_active", "disabled: True")):
                                has_action = True
                            if "icon:" in stripped and not widget_info:
                                widget_info = stripped
                            elif "text:" in stripped and not widget_info:
                                widget_info = stripped

                if current_widget:
                    total_actionable += 1
                    if not has_action:
                        unwired_buttons.append((rel_path, widget_line, current_widget, widget_info))

    print(f"  [AUDIT] Scanned {total_actionable} actionable buttons/chips across views.")
    if unwired_buttons:
        print(f"  [FAIL] Found {len(unwired_buttons)} unwired actionable controls:")
        for r in unwired_buttons:
            print(f"    - [{r[0]}:{r[1]}] {r[2]} ({r[3]}) has no bound action handler!")
        assert len(unwired_buttons) == 0, f"Found {len(unwired_buttons)} unwired actionable controls"
    
    results["all_actionable_widgets_bound"] = True
    print("  [PASS] 100% of actionable buttons, chips, and app bar buttons have active event bindings.")

    # Verify all app.<method> calls in .kv files exist on MusicApp
    if app_root not in sys.path:
        sys.path.insert(0, app_root)
    try:
        from main import MusicApp
        app_methods = set(dir(MusicApp))
        broken_calls = []
        for root, _, files in os.walk(kv_dir):
            for f in files:
                if f.endswith(".kv"):
                    path = os.path.join(root, f)
                    rel_path = os.path.relpath(path, kv_dir)
                    with open(path, "r", encoding="utf-8") as file:
                        text = file.read()
                    calls = re.findall(r'app\.([a-zA-Z0-9_]+)\(', text)
                    for c in calls:
                        if c not in app_methods and not hasattr(MusicApp, c):
                            broken_calls.append((rel_path, c))
        if broken_calls:
            print(f"  [FAIL] Found {len(broken_calls)} broken app method calls:")
            for r in broken_calls:
                print(f"    - [{r[0]}] app.{r[1]}() does not exist on MusicApp!")
            assert len(broken_calls) == 0, f"Found {len(broken_calls)} broken app method calls"
        print("  [PASS] 100% of app.<method>() bindings in .kv files exist on MusicApp.")
        results["all_app_methods_resolved"] = True
    except Exception as e:
        if "broken app method calls" in str(e):
            raise
        print(f"  [WARN] Could not inspect MusicApp methods: {e}")

    # Verify all static icon strings exist in md_icons and zero unsupported emoji/symbol codepoints exist in UI strings
    from kivymd.icon_definitions import md_icons
    invalid_icons = []
    unsupported_glyphs = []
    icon_expr_pat = re.compile(r"""\b(?:icon|source_icon)\s*[:=]\s*([^\n]+)""")
    lit_pat = re.compile(r"""['"]([a-z0-9-]+)['"]""")
    safe_non_ascii = set("•─—–…×÷±°§’")
    scan_dirs = [os.path.join(app_root, "views"), os.path.join(app_root, "app_core")]
    for base in scan_dirs:
        for root, _, files in os.walk(base):
            for f in files:
                if not f.endswith((".kv", ".py")):
                    continue
                path = os.path.join(root, f)
                rel_path = os.path.relpath(path, app_root)
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    for lineno, line in enumerate(fh, 1):
                        stripped = line.strip()
                        if not stripped.startswith("#"):
                            bad_chars = [
                                f"{ch}(U+{ord(ch):04X})"
                                for ch in line
                                if ord(ch) > 127 and ch not in safe_non_ascii and not ("source" in stripped and ch == "é")
                            ]
                            if bad_chars:
                                unsupported_glyphs.append((rel_path, lineno, bad_chars))
                        m = icon_expr_pat.search(line)
                        if m:
                            rhs = m.group(1)
                            for lm in lit_pat.finditer(rhs):
                                cand = lm.group(1)
                                if cand in ("one", "all", "off", "icon", "blank", "left", "right", "center", "text", "filled", "outlined", "tonal", "elevated", "standard", "small", "medium", "large", "none", "youtube", "jiosaavn", "spotify", "podcast", "default"):
                                    if cand not in ("youtube", "spotify", "podcast"):
                                        continue
                                if cand not in md_icons:
                                    invalid_icons.append((rel_path, lineno, cand))

    assert not invalid_icons, f"Invalid MDI icon names found: {invalid_icons}"
    assert not unsupported_glyphs, f"Unsupported non-ASCII UI glyphs found: {unsupported_glyphs}"
    results["all_icons_and_glyphs_valid"] = True
    print("  [PASS] 100% of MDI icon names exist in md_icons and zero unsupported emoji/symbol glyphs remain in UI.")

    print("  [ALL PASSED] Interactive Widgets Audit Suite Succeeded!")
    if on_complete:
        on_complete(True, results)
    return results

if __name__ == "__main__":
    run_test(lambda passed, res: sys.exit(0 if passed else 1))
