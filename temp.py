# fix_routes.py
import os
import re


def fix_template_routes():
    """Fix all route references in templates"""
    template_dir = "app/templates"

    for filename in os.listdir(template_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(template_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace 'main.stats' with 'main.statistics'
            fixed_content = content.replace(
                "url_for('main.stats')", "url_for('main.statistics')"
            )
            fixed_content = fixed_content.replace(
                'url_for("main.stats")', 'url_for("main.statistics")'
            )

            # Also fix active class check
            fixed_content = fixed_content.replace(
                "request.endpoint == 'main.stats'",
                "request.endpoint == 'main.statistics'",
            )

            if content != fixed_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(fixed_content)
                print(f"✅ Fixed {filename}")
            else:
                print(f"✅ {filename} is already correct")


def list_all_endpoints():
    """List all registered endpoints"""
    from app import create_app

    app = create_app()

    print("\n📋 Registered Endpoints:")
    print("-" * 50)

    endpoints = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith("main."):
            endpoints.append(
                {
                    "endpoint": rule.endpoint,
                    "route": rule.rule,
                    "methods": list(rule.methods),
                }
            )

    # Sort by endpoint name
    endpoints.sort(key=lambda x: x["endpoint"])

    for ep in endpoints:
        print(f"{ep['endpoint']:30} {ep['route']:40} {', '.join(ep['methods'])}")

    return endpoints


if __name__ == "__main__":
    print("🔧 Fixing template routes...")
    fix_template_routes()

    print("\n📋 Listing all endpoints...")
    list_all_endpoints()

    print("\n✅ Done! Run your app with: python run.py")
