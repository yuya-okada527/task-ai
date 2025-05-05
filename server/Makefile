ca:
	git add .
	git commit -m "update"
	git push origin head
run_mcp:
	uv run mcp_app.py
run_api:
	uv run api_app.py
test:
	IS_TEST_MODE=True uv run mcp_app.py
delete:
	echo "{}" > storage/event_store.json
