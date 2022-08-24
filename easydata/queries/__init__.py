from easydata.queries.clause import OrClause
from easydata.queries.jp import JMESPathSearch, JMESPathStrictSearch
from easydata.queries.key import KeySearch, KeyStrictSearch
from easydata.queries.pq import PyQuerySearch, PyQueryStrictSearch
from easydata.queries.re import ReSearch, ReStrictSearch

jp = JMESPathSearch
jp_strict = JMESPathStrictSearch

key = KeySearch
key_strict = KeyStrictSearch

orc = OrClause

pq = PyQuerySearch
pq_strict = PyQueryStrictSearch

re = ReSearch
re_strict = ReStrictSearch
