import json,subprocess,tempfile,unittest
from pathlib import Path
SCRIPT=Path(__file__).with_name('route.py')
class RoutingTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.r=Path(self.tmp.name);(self.r/'references').mkdir();(self.r/'memory').mkdir()
  (self.r/'references/catalog.json').write_text(json.dumps({'checked_on':'2026-11-08','materials':[{'name':'n8n-workflow-patterns','description':'Workflow automation','path':'skills/n8n/workflows/SKILL.md','sha':'a'*40}]}))
  (self.r/'references/source.json').write_text(json.dumps({'private_experience':True}))
 def tearDown(self):self.tmp.cleanup()
 def run_cli(self,*args,input=None):return subprocess.run(['python3',str(SCRIPT),'--root',str(self.r),*args],input=input,text=True,capture_output=True)
 def search(self,q,scope='general'):
  p=self.run_cli('search','--query',q,'--scope',scope);self.assertEqual(p.returncode,0,p.stderr);return json.loads(p.stdout)
 def test_excel_russian(self):self.assertEqual(self.search('Создать Excel табель')['candidates'][0]['name'],'Spreadsheets')
 def test_excel_no_cleaning(self):self.assertNotIn('ns-cleaning-kalkulator',[x['name'] for x in self.search('Excel табель')['candidates']])
 def test_n8n(self):self.assertIn('n8n-workflow-patterns',[x['name'] for x in self.search('n8n автоматизация')['candidates']])
 def test_unknown(self):self.assertEqual(self.search('zzqxxv')['candidates'],[])
 def test_output_bounded(self):self.assertLessEqual(len(self.search('pdf excel n8n реклама')['candidates']),3)
 def test_learning_dedup(self):
  n={'event_id':'sample-1','scope':'NS','tags':['excel'],'observation':'Repeated correction','recommendation':'Verify input dates','status':'candidate','evidence_kind':'observation'}
  for i in range(2):self.assertEqual(self.run_cli('learn',input=json.dumps(n)).returncode,0)
  self.assertEqual(len((self.r/'memory/experience.jsonl').read_text().splitlines()),1)
  self.assertEqual(len(self.search('excel','NS')['lessons']),1)
  self.assertEqual(len(self.search('excel','MDL')['lessons']),0)
 def test_invalid_note(self):self.assertNotEqual(self.run_cli('learn',input='{}').returncode,0)
 def test_public_checkout_refused(self):
  (self.r/'references/source.json').unlink();p=self.run_cli('learn',input='{}');self.assertNotEqual(p.returncode,0);self.assertIn('private',p.stderr)
 def test_bad_memory_skipped(self):
  (self.r/'memory/experience.jsonl').write_text('bad json\n');self.assertEqual(self.search('excel')['lessons'],[])
if __name__=='__main__':unittest.main()
