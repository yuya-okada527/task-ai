ca:
	git add .
	git commit -m "update"
	git push origin head
run_mcp:
	uv run mcp_app.py
run_api:
	uv run uvicorn api_app:app --reload --port 8001
test:
	IS_TEST_MODE=True uv run mcp_app.py
delete:
	echo "{}" > storage/event_store.json
