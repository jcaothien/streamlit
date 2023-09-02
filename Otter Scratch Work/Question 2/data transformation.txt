WITH
  transformed_raw AS(
/* This CTE consolidates and aggregates mult-row entries into a single date. 
For example Country 1, 10, 12, 13, 14,15, 6, 9 all have 1 row per day.
Countries 11 and 4 has 6 lines per day/partition
Countries 2 and 3  have 3 rows per day/partition
Country 5 has 2

My current assumption is that for each integration with a delivery partner, a row is generated for that partner. Therefore, for this exercise I am aggregating them.
*/



  SELECT
    day_partition,
    format_date("%Y-%Q",day_partition) as quarter,
    format_date("%Y-%m",day_partition) as month,
    region,
    country,
    -- general 
    
    SUM(Locations) AS locations,
    SUM(overall_daily_active) as overall_daily_active,
    SUM(overall_daily_access) as overall_daily_access,
    sum(overall_weekly_active) as overall_weekly_active,
    sum(overall_weekly_access) as overall_weekly_access,
    sum(overall_monthly_active) as overall_monthly_active,
    sum(overall_monthly_access) as overall_monthly_access,

    ## core
    sum(core_daily_active) as core_daily_active,
    sum(core_daily_access) as core_daily_access,
    sum(core_weekly_active) as core_weekly_active,
    sum(core_weekly_access) as core_weekly_access,
    sum(core_monthly_active) as core_monthly_active,
    sum(core_monthly_access) as core_monthly_access,

    ## premium
    sum(premium_daily_active) as premium_daily_active,
    sum(premium_daily_access) as premium_daily_access,
    sum(premium_weekly_active) as premium_weekly_active,
    sum(premium_weekly_access) as premium_weekly_access,
    sum(premium_monthly_active) as premium_monthly_active,
    sum(premium_monthly_access) as premium_monthly_access,
    
    ## promos
    sum(promos_daily_active) as promos_daily_active,
    sum(promos_daily_access) as promos_daily_access,
    sum(promos_weekly_active) as promos_weekly_active,
    sum(promos_monthly_active) as promos_monthly_active,
    sum(promos_monthly_access) as promos_monthly_access,

    ## custom websites
    sum(custom_websites_daily_active) as custom_websites_daily_active,
    sum(custom_websites_daily_access) as custom_websites_daily_access,
    sum(custom_websites_weekly_active) as custom_websites_weekly_active,
    sum(custom_websites_weekly_access) as custom_websites_weekly_access,
    sum(custom_websites_monthly_active) as custom_websites_monthly_active,
    sum(custom_websites_monthly_access) as custom_websites_monthly_access,

    ## premium custom websites
    sum(custom_websites_premium_daily_active) as custom_websites_premium_daily_active,
    sum(custom_websites_premium_daily_access) as custom_websites_premium_daily_access,
    sum(custom_websites_premium_weekly_active) as custom_websites_premium_weekly_active,
    sum(custom_websites_premium_weekly_access) as custom_websites_premium_weekly_access,
    sum(custom_websites_premium_monthly_access) as custom_websites_premium_monthly_active,
    sum(custom_websites_premium_monthly_access) as custom_websites_premium_monthly_access,

    ## basic_insights
    sum(basic_insights_daily_active) as basic_insights_daily_active,
    sum(basic_insights_daily_access) as basic_insights_daily_access,
    sum(basic_insights_weekly_active) as basic_insights_weekly_active,
    sum(basic_insights_weekly_access) as basic_insights_weekly_access,
    sum(basic_insights_monthly_active) as basic_insights_monthly_active,
    sum(basic_insights_monthly_access) as basic_insights_monthly_access,

    ## advance insights
    sum(adv_insights_daily_active) as adv_insights_daily_active,
    sum(adv_insights_daily_access) as adv_insights_daily_access,
    sum(adv_insights_weekly_active) as adv_insights_weekly_active,
    sum(adv_insights_weekly_access) as adv_insights_weekly_access,
    sum(adv_insights_monthly_active) as adv_insights_monthly_active,
    sum(adv_insights_monthly_access) as adv_insights_monthly_access,
    
    ## super insights
    sum(super_insights_daily_active) as super_insights_daily_active,
    sum(super_insights_daily_access) as super_insights_daily_access,
    sum(super_insights_weekly_active) as super_insights_weekly_active,
    sum(super_insights_weekly_access) as super_insights_weekly_access,
    sum(super_insights_monthly_active) as super_insights_monthly_active,
    sum(super_insights_monthly_access) as super_insights_monthly_access


  FROM
    `ottertakehome.productanalystdatadump.rawproductdata`
  GROUP BY
    country,
    day_partition,
    region,
    quarter,month
  ORDER BY
    1,
    2,
    3,
    4,
    5
  )

, stickiness as(

  select 

day_partition,
quarter,
month,
region,
country,
locations,
safe_divide(overall_daily_active, overall_monthly_active) as stickiness_overall,
safe_divide(core_daily_active, core_monthly_active) as stickiness_core,
safe_divide(premium_daily_active, premium_monthly_active) as stickiness_premium,
safe_divide(promos_daily_active, promos_monthly_active) as stickiness_promos,
safe_divide(custom_websites_daily_active, custom_websites_monthly_active) as stickiness_custom_websites,
safe_divide(custom_websites_premium_daily_active, custom_websites_premium_monthly_active) as stickiness_custom_websites_premium,
safe_divide(basic_insights_daily_active, basic_insights_monthly_active) as stickiness_basic_insights,
safe_divide(adv_insights_daily_active, adv_insights_monthly_active) as stickiness_adv_insights,
safe_divide(super_insights_daily_active, super_insights_monthly_active) as stickiness_super_insights

from transformed_raw
)

, adoption as (
SELECT
day_partition,
quarter,
month,
region,
country,
locations,

-----
#daily
safe_divide(overall_daily_active, overall_daily_access) as adoption_daily_overall,
safe_divide(core_daily_active, core_daily_access) as adoption_daily_core,
safe_divide(premium_daily_active, premium_daily_access) as adoption_daily_premium,
safe_divide(promos_daily_active, promos_daily_access) as adoption_daily_promos,
safe_divide(custom_websites_daily_active, custom_websites_daily_access) as adoption_daily_custom_websites,
safe_divide(custom_websites_premium_daily_active, custom_websites_premium_daily_access) as adoption_daily_custom_websites_premium,
safe_divide(basic_insights_daily_active, basic_insights_daily_access) as adoption_daily_basic_insights,
safe_divide(adv_insights_daily_active, adv_insights_daily_access) as adoption_daily_adv_insights,
safe_divide(super_insights_daily_active, super_insights_daily_access) as adoption_daily_super_insights,

---
#monthly
safe_divide(overall_monthly_active, overall_monthly_access) as adoption_monthly_overall,
safe_divide(core_monthly_active, core_monthly_access) as adoption_monthly_core,
safe_divide(premium_monthly_active, premium_monthly_access) as adoption_monthly_premium,
safe_divide(promos_monthly_active, promos_monthly_access) as adoption_monthly_promos,
safe_divide(custom_websites_monthly_active, custom_websites_monthly_access) as adoption_monthly_custom_websites,
safe_divide(custom_websites_premium_monthly_active, custom_websites_premium_monthly_access) as adoption_monthly_custom_websites_premium,
safe_divide(basic_insights_monthly_active, basic_insights_monthly_access) as adoption_monthly_basic_insights,
safe_divide(adv_insights_monthly_active, adv_insights_monthly_access) as adoption_monthly_adv_insights,
safe_divide(super_insights_monthly_active, super_insights_monthly_access) as adoption_monthly_super_insights


from transformed_raw
)

#select * from transformed_raw

, MonthlyIncrement AS (
  ## this helps with tracking new users per month
  SELECT
      day_partition,
      country,
      adv_insights_monthly_active - LAG(adv_insights_monthly_active, 1, 0) OVER (PARTITION BY country ORDER BY day_partition) AS adv_insights_monthly_increase,
      premium_monthly_active - LAG(premium_monthly_active, 1, 0) OVER (PARTITION BY country ORDER BY day_partition) AS premium_monthly_increase,
      custom_websites_premium_monthly_active - LAG(custom_websites_premium_monthly_active, 1, 0) OVER (PARTITION BY country ORDER BY day_partition) AS premium_custom_websites_monthly_increase,
      EXTRACT(YEAR FROM day_partition) AS year
    FROM transformed_raw
)

, revenue AS (
    select 
  t.day_partition,
  t.region,
  t.country,
  t.locations,

-----CORE-----
   # Counts all usage in the past month and bills according to the active. This is a simple estimate, since billing cycles can occur everyday, however, not enough data to determine that.
   CASE
    WHEN t.day_partition = last_day(t.day_partition,MONTH) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          core_monthly_active * 5
        WHEN  t.region = 'Region 2' THEN
          core_monthly_active  * 5
        WHEN t.region = 'Region 3' THEN
          core_monthly_active * 20
      END
    ELSE
      0
  END AS core_monthly_revenue,


  -----PREMIUM-----

## monthly revenue is calculated at months end.
  CASE
    WHEN t.day_partition = last_day(t.day_partition,MONTH) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          premium_monthly_active * 20
        WHEN  t.region = 'Region 2' THEN
          premium_monthly_active  * 30
        WHEN t.region = 'Region 3' THEN
          premium_monthly_active * 80
      END
      ELSE
      0
  END AS premium_monthly_revenue,

## Activation revenue determined at new actives using the feature. The increment is determined by day-over-day changes
mi.premium_monthly_increase as incremental_new_premium_actives,
  CASE
    WHEN mi.premium_monthly_increase > 0 THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          mi.premium_monthly_increase * 100
        WHEN  t.region = 'Region 2' THEN
          mi.premium_monthly_increase * 150
        WHEN  t.region = 'Region 3' THEN
        mi.premium_monthly_increase * 200
      END
    ELSE
      0
  END AS premium_activation_revenue,

-----OTHER FEATURES-----

##CUSTOM WEBSITE MONTHLY REVENUE
  # Counts all usage in the past month and bills according to the active. This is a simple estimate, since billing cycles can occur everyday, however, not enough data to determine that.
   CASE
    WHEN t.day_partition = last_day(t.day_partition,MONTH) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          custom_websites_monthly_active * 5
        WHEN  t.region = 'Region 2' THEN
          custom_websites_monthly_active  * 5
        WHEN t.region = 'Region 3' THEN
          custom_websites_monthly_active * 20
      END
    ELSE
      0
  END AS custom_website_monthly_revenue,

## PROMOS REVENUE
  # Counts all usage in the past month and bills according to the active. This is a simple estimate, since billing cycles can occur everyday, however, not enough data to determine that.
   CASE
    WHEN t.day_partition = last_day(t.day_partition,MONTH) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          promos_monthly_active * 20
        WHEN  t.region = 'Region 2' THEN
          promos_monthly_active  * 15
        WHEN t.region = 'Region 3' THEN
          promos_monthly_active * 80
      END
    ELSE
      0
  END AS promos_monthly_revenue,

  -----INSIGHTS-----
## BASIC INSIGHTS REVENUE
# Counts all usage in the past month and bills according to the active. This is a simple estimate, since billing cycles can occur everyday, however, not enough data to determine that.
   CASE
    WHEN t.day_partition = last_day(t.day_partition,MONTH) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          basic_insights_monthly_active * 5
        WHEN  t.region = 'Region 2' THEN
          basic_insights_monthly_active  * 5
        WHEN t.region = 'Region 3' THEN
          basic_insights_monthly_active * 10
      END
    ELSE
      0
  END AS basic_insights_monthly_revenue,


## ADVANCED INSIGHTS REVENUE
  # This logic assumes that once a person uses the feature, they are billed for the year and only pay once for the year. This looks at the incremental growth in monthly users, and applies the $10 or $60 to the net new active users.This resets when the year changes.
  CASE
    WHEN mi.adv_insights_monthly_increase > 0 AND mi.year <= EXTRACT(YEAR FROM t.day_partition) THEN
      CASE
        WHEN t.region = 'Region 1' THEN
          mi.adv_insights_monthly_increase * 10
        WHEN t.region = 'Region 2' THEN
          mi.adv_insights_monthly_increase * 10
        WHEN t.region = 'Region 3' THEN
        mi.adv_insights_monthly_increase * 60
        ELSE
          mi.adv_insights_monthly_increase * 10
      END
    ELSE
      0
  END AS adv_insights_annual_revenue,

## SUPER INSIGHTS REVENUE
  # since super_insights_daily are charged as one-off, im interpretting this to mean everytime a super insight is provided, charge $20. Therefore, it makes sense to look at daily actives.
  case 
      when region = "Region 1" THEN super_insights_daily_active * 20
      when region = "Region 2" THEN super_insights_daily_active * 25
      when region = "Region 3" THEN super_insights_daily_active * 30
      when region = "Region 4" THEN super_insights_daily_active * 20
      when region = "Region 5" THEN super_insights_daily_active * 20

      end as super_insights_revenue

from transformed_raw t
left JOIN MonthlyIncrement mi ON t.day_partition = mi.day_partition AND t.country = mi.country

order by 3,1,1
)


, final as(


  select 

  -----general-----
  t.day_partition,
  t.region,
  t.country,
  t.locations,

  -----overall-----
t.overall_daily_active,
t.overall_daily_access,
t.overall_monthly_active,
t.overall_monthly_access,
s.stickiness_overall,
a.adoption_daily_overall,
a.adoption_monthly_overall,
(r.core_monthly_revenue + r.premium_activation_revenue + r.premium_monthly_revenue + r.promos_monthly_revenue + r.custom_website_monthly_revenue + r.basic_insights_monthly_revenue + r.adv_insights_annual_revenue + r.super_insights_revenue) as overall_revenue,

  -----core-----
t.core_daily_active,
t.core_daily_access,
t.core_monthly_active,
t.core_monthly_access,
s.stickiness_core,
a.adoption_daily_core,
a.adoption_monthly_core,
r.core_monthly_revenue,

   -----premium-----
t.premium_daily_active,
t.premium_daily_access,
t.premium_monthly_active,
t.premium_monthly_access,   
s.stickiness_premium,
a.adoption_daily_premium,
a.adoption_monthly_premium,
r.premium_activation_revenue,
r.premium_monthly_revenue,

-----website-----
t.custom_websites_daily_active,
t.custom_websites_daily_access,
t.custom_websites_monthly_active,
t.custom_websites_monthly_access,
s.stickiness_custom_websites,
a.adoption_daily_custom_websites,
a.adoption_monthly_custom_websites,
r.custom_website_monthly_revenue,

-----insights-----

#basic_insights
t.basic_insights_daily_active,
t.basic_insights_daily_access,
t.basic_insights_monthly_active,
t.basic_insights_monthly_access,
s.stickiness_basic_insights,
a.adoption_daily_basic_insights,
a.adoption_monthly_basic_insights,
r.basic_insights_monthly_revenue,

#adv_insights
t.adv_insights_daily_active,
t.adv_insights_daily_access,
t.adv_insights_monthly_active,
t.adv_insights_monthly_access,
s.stickiness_adv_insights,
a.adoption_daily_adv_insights,
a.adoption_monthly_adv_insights,
r.adv_insights_annual_revenue,

#super_insights 
t.super_insights_daily_active,
t.super_insights_daily_access,
t.super_insights_monthly_active,
t.super_insights_monthly_access,
s.stickiness_super_insights,
a.adoption_daily_super_insights,
a.adoption_monthly_super_insights,
r.super_insights_revenue,

  from transformed_raw t
  left join stickiness s ON t.day_partition = s.day_partition AND t.country = s.country
  left join adoption a ON t.day_partition = a.day_partition AND t.country = a.country
  left join revenue r ON t.day_partition = r.day_partition AND t.country = r.country

)
select * from final
order by 3,1,1

