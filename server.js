const express = require("express");
const http = require("http");
const socketIo = require("socket.io");
const pty = require("node-pty");
const AnsiToHtml = require("ansi-to-html");
const ansiToHtml = new AnsiToHtml();

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const basicAuth = require("express-basic-auth");

app.use(basicAuth({
  users: { 'admin': 'blitzproxy' },
  challenge: true,
  unauthorizedResponse: (req) => "Access denied"
}));

app.use(express.static("public"));

let shellProcess = null;
let outputBuffer = "";
const fs = require("fs");
const path = require("path");

app.use(express.json());
const allowedDirs = ["out-files", "raw-files"];

app.get("/api/files", (req, res) => {
    const result = {};
    for (const dir of ["out-files", "raw-files"]) {
        const fullPath = path.join(__dirname, dir);
        if (fs.existsSync(fullPath)) {
            result[dir] = fs.readdirSync(fullPath).filter(f => f.endsWith(".txt"));
        } else {
            result[dir] = [];
        }
    }
    res.json(result);
});


app.get("/api/file", (req, res) => {
    const { folder, filename } = req.query;
    if (!allowedDirs.includes(folder)) return res.status(403).send("Access denied");
    const filePath = path.join(__dirname, folder, filename);
    if (!fs.existsSync(filePath)) return res.status(404).send("file not found");
    const content = fs.readFileSync(filePath, "utf-8");
    res.send(content);
});

io.on("connection", (socket) => {
    console.log("[SERVER] Client connected via GUI");
    socket.emit("full-buffer", outputBuffer);

    socket.on("start-script", () => {
        if (!shellProcess) {
            console.log("[SCRIPT] Launching proxy modules...");
            shellProcess = pty.spawn("/bin/bash", ["run.sh"], {
                name: "xterm-color",
                cols: 80,
                rows: 24,
                cwd: process.cwd(),
                env: process.env
            });

            shellProcess.on("data", (data) => {
                outputBuffer += data;
                io.emit("output", data);
            });

            shellProcess.on("exit", () => {
                console.log("[SCRIPT] Process exited successfully");
                shellProcess = null;
            });
        }
    });

    socket.on("stop-script", () => {
        if (shellProcess) {
            shellProcess.kill();
            shellProcess = null;
            console.log("[SCRIPT] Execution manually terminated by user");
        }
    });

    socket.on("disconnect", () => {
        console.log("[SERVER] Client disconnected from GUI");
    });
});

server.listen(3000, "0.0.0.0", () => {
    console.log("[SERVER] Web interface available at http://0.0.0.0:3000");
});