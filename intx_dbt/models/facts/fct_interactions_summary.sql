-- models/facts/fct_interactions_summary.sql
-- Aggregated fact table for interactions

with interactions_staged as (
    select *
    from {{ ref('stg_interactions') }}
)

select
    category,
    count(*) as total_interactions,
    avg(duration_minutes) as avg_duration,
    avg(factor_score) as avg_factor_score,
    min(date) as first_interaction,
    max(date) as last_interaction
from interactions_staged
group by category
