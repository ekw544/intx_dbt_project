-- models/staging/stg_interactions.sql
-- Staging model for simulated interactions

with raw as (
    select *
    from interactions
)

select
    interaction_id,
    participant,
    date,
    category,
    duration_minutes,
    factor_score
from raw