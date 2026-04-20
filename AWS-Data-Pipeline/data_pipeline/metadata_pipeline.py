import json

def generate_silver_query(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)

    cfg = config["silver_layer"]

    columns = ",\n    ".join(cfg["columns"])

    derived_cols = ",\n    ".join([
        f"{expr} AS {name}"
        for name, expr in cfg["derived_columns"].items()
    ])

    query = f"""
    CREATE OR REPLACE VIEW {cfg['target_view']} AS
    SELECT
        {columns},
        {derived_cols}
    FROM {cfg['source_table']}
    """

    return query

if __name__ == "__main__":
    sql = generate_silver_query("config/pipeline_config.json")
    print(sql)