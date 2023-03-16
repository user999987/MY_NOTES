commad+shift+p open user settings(JSON)
edit file:
```
{
    "editor.fontSize": 14,
    "terminal.integrated.fontSize": 14
}
```

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [

        {
            "name": "Launch Package",
            "type": "go",
            "request": "launch",
            "mode": "auto",
            "program": "${workspaceFolder}/cmd/",//program entry point
            "cwd":"${workspaceFolder}" // working directory of the application launched by the debugger.
        }
    ]
}
```