drop table if exists messages;

create table messages(
  id integer primary key autoincrement,
  'user' text not null,
  'message' text not null,
  'room' text not null
)
