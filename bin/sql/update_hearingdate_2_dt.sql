UPDATE cases_summary
SET hearingdatetime =
CASE
WHEN RIGHT(hearingdate,2) = 'AM' THEN
TO_TIMESTAMP(
    hearingdate,
    'MM/DD/YYYY, HH:MI AM'
)
WHEN RIGHT(hearingdate,2) = 'PM' THEN
TO_TIMESTAMP(
    hearingdate,
    'MM/DD/YYYY, HH:MI PM'
)
END;