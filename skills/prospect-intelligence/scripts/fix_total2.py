with open('audit.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Replace lines 927-935 (0-indexed)
new_lines = lines[:927]

new_section = """        if bundle.get("is_rebuild"):
            # For rebuilds: show rebuild cost only (automations included)
            rebuild_low = bundle.get("rebuild_price_low", 3500)
            rebuild_high = bundle.get("rebuild_price_high", 6500)
            monthly_recurring = sum(s.get("price", 0) for s in bundle.get("implementation_services", []) if "/mo" in s.get("price_display", ""))
            
            html += f\"\"\"
    </table>
    <div class=\"highlight-box\">
        <p><strong>Total Investment:</strong> €{rebuild_low:,} – €{rebuild_high:,} (one-time rebuild)</p>
        {f'<p><strong>Monthly recurring:</strong> €{monthly_recurring:,}/month for included services</p>' if monthly_recurring > 0 else ''}
        <p style=\"color: #666; font-size: 0.9em; margin-top: 10px;\">All automations listed above are included in the rebuild price. No additional implementation fees.</p>
    </div>
</div>\"\"\"
        else:
            total = bundle.get("entry_price", 0) + bundle.get("total_implementation", 0)
            html += f\"\"\"
    </table>
    <div class=\"highlight-box\">
        <p><strong>Total Investment (à la carte):</strong> €{total:,}</p>
        {f"<p><strong>Growth Package:</strong> €{bundle.get('growth_package', {}).get('price', 0):,} (save €{bundle.get('growth_savings', 0):,})</p>" if bundle.get('growth_package_recommended') else ''}
    </div>
</div>\"\"\"

"""

new_lines.append(new_section)
new_lines.extend(lines[935:])

with open('audit.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('SUCCESS')
