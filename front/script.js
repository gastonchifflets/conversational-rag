const input = document.querySelector("#text")
const sender = document.querySelector("#text-sender")
const messagesContainer = document.querySelector("#messages-container")
const loader = document.querySelector("#loader")

input.addEventListener('keypress', function(e) {
  if (e.key === 'Enter' && e.target.value.length > 0) {
    sendUserMessage()
  }
})

sender.addEventListener("click", function (e) {
  if (input.value.length > 0) sendUserMessage()
})

async function sendUserMessage() {
  try {
    const text = input.value
    input.value = ""
    input.disabled = true
    input.style.backgroundColor = "#605f5f"
    messagesContainer.innerHTML += `<span class="message user-message">${text}</span>`
    loader.className = "loader"
    const response = await fetch('http://3.16.70.184:8501/', {
      method: "POST",
      body: JSON.stringify({ input: text }),
    })
    const IAresponse = await response.json()
    messagesContainer.innerHTML += `<span class="message">${IAresponse}</span>`
  } catch (error) {
    console.log(error)
    alert("There was an error getting the response. Please contact me at gastonchifflets@gmail.com.")
  } finally {
    loader.className = ""
    input.disabled = false
    input.style.backgroundColor = "#201e1e"
  }
}