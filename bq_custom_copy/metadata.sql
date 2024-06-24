Create or replace table deepak.table_copy (
  tcid int64,
  source_project string,
  source_dataset string,
  source_table string,
  target_project string,
  target_dataset string,
  target_table string,
  is_active boolean

);
select * from deepak.table_copy ;
insert into deepak.table_copy values (1,'mlconsole-poc','deepak','aborted_email','mlconsole-poc','Ashok','aborted_email', true);
insert into deepak.table_copy values (2,'mlconsole-poc','Ashok','Produce','mlconsole-poc','deepak','Produce',true);

--0 2 * * 6 /home/path/dataload.sh >>/home/path/logfile.log  2>&1