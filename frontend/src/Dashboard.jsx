import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Card,
  Grid,
  Button,
  Modal,
  Avatar,
  TextField
} from "@mui/material";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

export default function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState("dashboard");
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/violations")
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(err => console.error(err));
  }, []);

  // ===== SUMMARY =====
  const summary = {
    helmetless: logs.filter(l => l.Violation === "helmetless").length,
    triple_riding: logs.filter(l => l.Violation === "triple_riding").length,
    wrong_way: logs.filter(l => l.Violation === "wrong_way").length,
    mobile_usage: logs.filter(l => l.Violation === "mobile_usage").length,
  };

  const chartData = Object.entries(summary).map(([k, v]) => ({
    name: k.replace("_", " "),
    value: v
  }));

  const mostViolation =
    chartData.sort((a, b) => b.value - a.value)[0]?.name || "None";

  const darkCard = {
    bgcolor: "#1e293b",
    color: "white",
    p: 3,
    borderRadius: 3,
    textAlign: "center"
  };

  return (
    <Box sx={{ display: "flex", height: "100vh", bgcolor: "#f4f6f9" }}>

      {/* ================= SIDEBAR ================= */}
      <Box sx={{
        width: 240,
        bgcolor: "#f1f5f9",
        borderRight: "1px solid #e5e7eb",
        p: 3
      }}>
        <Typography sx={{ fontWeight: 700, mb: 4 }}>
          Governance Portal
        </Typography>

        {["dashboard", "analytics", "location map", "challan"].map(p => (
          <Button
            key={p}
            fullWidth
            sx={{ justifyContent: "flex-start", mb: 2 }}
            onClick={() => setPage(p)}
          >
            {p}
          </Button>
        ))}
      </Box>

      {/* ================= MAIN ================= */}
      <Box sx={{ flex: 1 }}>

        {/* HEADER */}
        <Box sx={{
          bgcolor: "white",
          p: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "1px solid #e5e7eb"
        }}>
          <Box>
            <Typography sx={{ fontSize: 22, fontWeight: 600 }}>
              Dashboard Overview
            </Typography>
            <Typography sx={{ color: "gray" }}>
              Smart Traffic Governance System
            </Typography>
          </Box>

          <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
            <TextField size="small" placeholder="Search..." />
            <Avatar sx={{ bgcolor: "#6366f1" }}>A</Avatar>
          </Box>
        </Box>

        {/* CONTENT */}
        <Box sx={{ p: 5, overflowY: "auto", height: "calc(100vh - 100px)" }}>

          {/* ================= DASHBOARD ================= */}
          {page === "dashboard" && (
            <>
              <Typography sx={{ fontSize: 28, mb: 4 }}>
                SPATIO-TEMPORAL TRAFFIC VIOLATION DETECTION
              </Typography>

              {/* SUMMARY */}
              <Grid container spacing={3} sx={{ mb: 4 }}>
                {Object.entries(summary).map(([k, v]) => (
                  <Grid item xs={3} key={k}>
                    <Card sx={darkCard}>
                      <Typography>{k.replace("_", " ")}</Typography>
                      <Typography sx={{ fontSize: 28, fontWeight: 700 }}>
                        {v}
                      </Typography>
                    </Card>
                  </Grid>
                ))}
              </Grid>

              {/* ALERT */}
              <Card sx={{ p: 3, mb: 4, bgcolor: "#fee2e2" }}>
                🚨 High Violation Activity Detected: {mostViolation}
              </Card>

              {/* VIDEO */}
              <Card sx={{ p: 3, borderRadius: 3 }}>
                <Typography sx={{ mb: 2 }}>
                  Processed Output Video
                </Typography>
                <video
                  src="http://127.0.0.1:5000/videos/helmetless_fixed.mp4"
                  controls
                  style={{
                    width: "100%",
                    maxHeight: 350,
                    borderRadius: 8
                  }}
                />
              </Card>
            </>
          )}

          {/* ================= ANALYTICS ================= */}
          {page === "analytics" && (
            <>
              <Typography sx={{ fontSize: 24, mb: 3 }}>
                Violation Analytics
              </Typography>

              <Card sx={{ p: 3, mb: 4 }}>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="value"
                      stroke="#6366f1"
                      strokeWidth={3}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Card>

              <Card sx={{ p: 3, bgcolor: "#e0e7ff" }}>
                <Typography sx={{ fontSize: 18 }}>
                  Most Frequent Violation:
                </Typography>
                <Typography sx={{ fontSize: 22, fontWeight: 600 }}>
                  {mostViolation}
                </Typography>
              </Card>
            </>
          )}

          {/* ================= LOCATION MAP ================= */}
          {page === "location map" && (
            <Card sx={{ p: 3 }}>
              <Typography sx={{ mb: 2 }}>
                Saranathan College Road – Violation Zone
              </Typography>
              <iframe
                width="100%"
                height="450"
                style={{ borderRadius: 10 }}
                src="https://www.google.com/maps?q=Saranathan+College+Road+Trichy&output=embed"
              />
            </Card>
          )}

          {/* ================= CHALLAN ================= */}
          {page === "challan" && (
            <>
              {logs.map((row, i) => (
                <Card key={i} sx={{ p: 3, mb: 2 }}>
                  <Typography sx={{ fontWeight: 600 }}>
                    {row.Violation}
                  </Typography>
                  <Typography>{row.Time}</Typography>

                  <Button
                    variant="contained"
                    sx={{ mt: 2 }}
                    onClick={() => setSelected(row)}
                  >
                    Open Challan
                  </Button>
                </Card>
              ))}
            </>
          )}
        </Box>
      </Box>

      {/* ================= CHALLAN MODAL ================= */}
      <Modal open={Boolean(selected)} onClose={() => setSelected(null)}>
        <Box sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: 450,
          bgcolor: "white",
          p: 4,
          borderRadius: 3
        }}>
          {selected && (
            <>
              <Typography sx={{ fontSize: 22, mb: 2 }}>
                Traffic Challan
              </Typography>

              <Typography>Violation: {selected.Violation}</Typography>
              <Typography>Date & Time: {selected.Time}</Typography>
              <Typography>Location: Saranathan Road</Typography>

              <img
                src={`http://127.0.0.1:5000/snapshots/${selected.Snapshot?.split("/").pop()}`}
                width="100%"
                style={{ borderRadius: 8, marginTop: 10 }}
              />
            </>
          )}
        </Box>
      </Modal>
    </Box>
  );
}