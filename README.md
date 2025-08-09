- 👋 Hi, I’m @affixabidita89
- 👀 I’m interested in Quality Assurance
- 🌱 I’m currently learning Robot Framework, Flutter, Web Development
- 💞️ I’m looking to collaborate on ...
- 📫 How to reach me ...

<!---
affixabidita89/affixabidita89 is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Wibu Score API
A simple HTTP server that computes how "wibu" someone is based on answers to five questions.

### Running locally
```bash
python app.py
```

### Example request
```bash
curl -X POST http://localhost:8000/wibu-score \
  -H "Content-Type: application/json" \
  -d '{"answers":[true,true,false,true,false]}'
```
