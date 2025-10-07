# Field-Focused Extraction Guide

This guide shows how to configure PDF types to extract only the fields you're interested in.

## New Transform Operations

### 1. `select_fields` - Choose Specific Columns
```yaml
transforms:
  - op: select_fields
    fields: ["Product", "Q1", "Q2", "Q3", "Q4", "Total"]
    allow_missing: false  # Error if any field is missing
```

### 2. `filter_by_field_values` - Filter Rows by Field Values
```yaml
transforms:
  - op: filter_by_field_values
    field: "Department"
    values: ["Engineering", "Marketing", "Sales"]
    keep: true  # Keep only these departments
```

### 3. `extract_field_subset` - Combined Field Selection and Filtering
```yaml
transforms:
  - op: extract_field_subset
    config:
      fields: ["Employee ID", "Name", "Salary"]
      filter_field: "Department"
      filter_values: ["Engineering"]
      filter_keep: true
      allow_missing_fields: true
```

## Example Rules Files

### Employee Focus (`rules/employee_focus.yml`)
- Extracts only employee data
- Filters by specific departments and positions
- Keeps only relevant fields: ID, Name, Department, Position, Salary, Start Date

### Financial Metrics Only (`rules/financial_metrics_only.yml`)
- Focuses on key financial metrics
- Excludes detailed breakdowns
- Filters to Revenue, Net Profit, ROI only

### Rural Adjustment Enhanced (`rules/sample_rural_adj.yml`)
- Selects only product sales fields
- Filters to specific widget products
- Renames columns for consistency

## Usage Examples

```bash
# Extract only employee data with department filtering
python cli.py employee_report.pdf --pdf-type employee_focus --rules ./rules

# Focus on financial metrics only
python cli.py financial_summary.pdf --pdf-type financial_metrics_only --rules ./rules

# Batch process with field focus
python batch_extract_excel.py ./reports ./output --pdf-type employee_focus --rules ./rules
```

## Benefits

1. **Reduced Data Volume**: Only extract fields you need
2. **Cleaner Output**: No irrelevant columns or rows
3. **Faster Processing**: Less data to process and transform
4. **Consistent Structure**: Same fields across all PDFs of the same type
5. **Easy Analysis**: Pre-filtered data ready for analysis

## Field Selection Strategies

- **By Column Names**: Use `select_fields` with exact column names
- **By Row Values**: Use `filter_by_field_values` to keep/exclude specific rows
- **Combined Approach**: Use `extract_field_subset` for complex filtering
- **Flexible Missing Fields**: Set `allow_missing: true` for optional fields
