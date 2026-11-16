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
    print("  [ALL PASSED] Interactive Widgets Audit Suite Succeeded!")
    if on_complete:
        on_complete(True, results)
    return results

if __name__ == "__main__":
    run_test(lambda passed, res: sys.exit(0 if passed else 1))
