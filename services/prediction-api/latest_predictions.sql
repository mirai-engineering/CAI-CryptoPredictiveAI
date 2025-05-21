drop materialized view if exists :view_name;
create materialized view :view_name as
with latest_predictions as (
    select
        pair,
        max(ts_ms) as last_ts
    from :table_name
    group by 1
)

select
    p.pair,
    p.predicted_price,
    p.ts_ms,
    p.predicted_ts_ms
from
    public.predictions p
    inner join latest_predictions lp
        on p.pair = lp.pair and p.ts_ms = lp.last_ts
;