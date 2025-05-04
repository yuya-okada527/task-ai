# task-ai

## 概要

これは、タスク管理アプリです。エージェントファースト業務アプリケーションの形を模索するためのプロトタイプとして、イベントソーシング×MCPで実装を行います。デモ目的の簡易的な作りのため、初期実装ではイベントストアはインメモリで実装し、CQRSも実装しません。

## 機能

- [ ] タスクの追加
- [ ] タスクの編集
- [ ] タスク一覧の表示
- [ ] タスク詳細の参照
- [ ] タスクの変更履歴閲覧
- [ ] タスクの状態復元

## 技術スタック

- 言語: Python
- イベントストア: インメモリ

## データモデル

- タスク(task)

```mermaid
classDiagram
    class Task {
        +id: str
        +title: str
        +description: str
        +status: enum~str~
    }
```

- ステータス(status)
  - todo
  - in_progress
  - done

## イベント

- TaskCreated

サンプル
```json
{
  "event_id": "1234567890",
  "task_id": "12345",
  "event_type": "TaskCreated",
  "payload": {
    "title": "タスクのタイトル",
    "description": "タスクの説明",
    "status": "todo"
  }
}
```

- TaskUpdated

サンプル
```json
{
  "event_id": "1234567890",
  "task_id": "12345",
  "event_type": "TaskUpdated",
  "payload": {
    "title": "タスクのタイトル",
    "description": "タスクの説明",
    "status": "in_progress"
  }
}
```

