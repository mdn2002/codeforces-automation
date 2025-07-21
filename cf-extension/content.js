(async () => {
  const html = document.documentElement.outerHTML;
  const url = window.location.href;
  await fetch("http://localhost:8765/receive", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ html, url })
  });
  alert("Codeforces problem HTML sent to your script!");
})(); 