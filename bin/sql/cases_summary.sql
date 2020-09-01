CREATE TABLE public.cases_summary
(
  courtname text NOT NULL,
  case_num text NOT NULL,
  defendant text NOT NULL,
  complainant text NOT NULL,
  hearingdate text NOT NULL,
  amended_charge BOOL NOT NULL,
  charge text,
  result text
  PRIMARY KEY (case_num, date)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.cases_summary
  OWNER TO alex;