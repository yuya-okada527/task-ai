"use client";

import { useChat } from "@ai-sdk/react";
import { useEffect, useState } from "react";

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, status } = useChat();
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    async function fetchTasks() {
      try {
        const response = await fetch("http://localhost:8001/api/tasks");
        if (response.ok) {
          const data = await response.json();
          setTasks(data.tasks);
        } else {
          console.error("Failed to fetch tasks");
        }
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    }

    fetchTasks();
  }, []);

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto gap-4">
      <h1 className="text-2xl font-bold">Chat with OpenAI</h1>

      <div className="task-view">
        <h2 className="text-xl font-semibold">Tasks</h2>
        <ul className="list-disc pl-5">
          {tasks.map((task) => (
            <li key={task.task_id}>
              <div><strong>Title:</strong> {task.title}</div>
              <div><strong>Description:</strong> {task.description}</div>
              <div><strong>Status:</strong> {task.status}</div>
            </li>
          ))}
        </ul>
      </div>

      {messages.map((message) => (
        <div key={message.id} className="whitespace-pre-wrap">
          {message.role === "user" ? "User: " : "AI: "}
          {message.parts.map((part, i) => {
            switch (part.type) {
              case "text":
                return <div key={`${message.id}-${i}`}>{part.text}</div>;
            }
          })}
        </div>
      ))}

      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <input
          type="text"
          value={input}
          onChange={handleInputChange}
          className="w-full p-2 border border-gray-300 rounded dark:disabled:bg-gray-700"
          placeholder="Type your message..."
          disabled={status !== "ready"}
        />
        <button
          type="submit"
          className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600 disabled:bg-gray-700"
          disabled={status !== "ready"}
        >
          {status !== "ready" ? "🤔" : "Send"}
        </button>
      </form>
    </div>
  );
}