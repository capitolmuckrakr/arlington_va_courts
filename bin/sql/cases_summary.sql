CREATE TABLE cases_summary
(
  courtname text NOT NULL,
  case_num text NOT NULL,
  defendant text NOT NULL,
  complainant text NOT NULL,
  hearingdate text NOT NULL,
  amended_charge BOOL NOT NULL,
  charge text,
  result text,
  PRIMARY KEY (case_num, hearingdate)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE cases_summary
  OWNER TO alex;