// Constants for embed mode and UI elements
// import {lightMode, darkMode, setProperties} from "./constants.js";


// Themes
const lightMode = {
  body_bg: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
  msger_bg: '#fff',
  border: '1px solid #ddd',
  left_msg_bg: '#ececec',
  left_msg_txt: 'black',
  right_msg_bg: 'rgb(140, 0, 255)',
  msg_header_bg: 'rgba(238,238,238,0.75)',
  msg_header_txt: '#666',
  clear_btn_txt: '#999',
  msg_chat_bg_scrollbar: '#ddd',
  msg_chat_bg_thumb: '#bdbdbd',
  msg_chat_bg: '#fcfcfe',
  msg_input_bg: '#ddd',
  msg_input_area_bg: '#eee',
  msg_invert_image: 'invert(0%)',
  msg_input_color: "black",
  right_msg_txt: 'white',
  // legacy, not used
  imessageInterface_: {
    display_images: 'block',
    border_radius_all: '15px',
    msg_bubble_max_width: '450px',
    msg_bubble_width: 'unset',
    msg_margin: '5px',
    msg_chat_padding: '10px',
    right_msg_txt: 'white',
    msg_padding: '0',
    right_msg_bg_bgd: 'transparent',
  },
  // this is the interface
  normalInterface_: {
    display_images: 'none',
    border_radius_all: '0px',
    msg_bubble_max_width: 'unset',
    msg_bubble_width: '100%',
    msg_margin: '0',
    msg_chat_padding: '0',
    msg_chat_bg: '#f1f1f1',
    right_msg_bg: 'white',
    right_msg_txt: 'black',
    left_msg_bg: 'transparent',
    msg_padding: '5px 20px',
    right_msg_bg_bgd: 'white',
  }

}

const darkMode = {
  body_bg: 'linear-gradient(135deg, #3e3c46 0%, #17232c 100%)',
  msger_bg: '#2d2d2d',
  border: '1px solid #2d2d2d',

  left_msg_txt: 'white',
  right_msg_bg: 'rgb(140, 0, 255)',
  msg_header_bg: 'rgba(41,41,41,0.75)',
  msg_header_txt: '#d5d5d5',
  clear_btn_txt: '#e5e5e5',
  msg_chat_bg_scrollbar: 'transparent',
  msg_chat_bg_thumb: '#656172',
  msg_input_bg: '#2f2f2f',
  msg_input_area_bg: '#252525',
  msg_invert_image: 'invert(100%)',
  msg_input_color: "white",
  right_msg_txt: 'white',
  msg_chat_bg: '#3e3c46',
  // legacy, not used
  imessageInterface_: {
    display_images: 'block',
    border_radius_all: '15px',
    msg_bubble_max_width: '450px',
    msg_bubble_width: 'unset',
    msg_margin: '5px',
    msg_chat_padding: '10px',
    right_msg_txt: 'white',
    right_msg_bg: 'rgb(140, 0, 255)',
    msg_header_bg: 'rgba(48,48,59,0.75)',
    msg_input_area_bg: '#3e3c46',
    msg_input_bg: '#2e2e33',
    left_msg_bg: '#302f36',
    msg_padding: '0',
    right_msg_bg_bgd: 'transparent',
  },
  // this is the interface
  normalInterface_: {
    msg_chat_bg_scrollbar: '#52505b',
    display_images: 'none',
    border_radius_all: '10px',
    msg_bubble_max_width: 'unset',
    msg_bubble_width: '100%',
    msg_margin: '0',
    msg_chat_padding: '0',
    right_msg_bg: '#302f36',
    right_msg_txt: 'white',
    msg_header_bg: 'rgba(48,48,59,0.75)',
    msg_input_area_bg: '#3e3c46',
    left_msg_bg: 'transparent',
    msg_input_bg: '#2e2e33',
    msg_padding: '5px 20px',
    right_msg_bg_bgd: '#302f36',
  }
}

function setProperties() {
    const theme = localStorage.getItem('theme')
    const interfaceTheme = 'normal'
  const object = theme === 'dark' ? darkMode : lightMode
  const interfaceObject = interfaceTheme === 'normal' ? object.normalInterface_ : object.imessageInterface_
  setPropertiesHelper(object)
  setPropertiesHelper(interfaceObject)
    console.log("DKFSDKKH")
}
function setPropertiesHelper(themeObject) {

  for (let key in themeObject) {
    if(key.endsWith('_')) {

    } else {
      const property_replaced = key.replace(/_/g, '-')
      const property_name = `--${property_replaced}`
      console.log(property_name)
      const value = themeObject[key]

      document.documentElement.style.setProperty(property_name, value)
    }
  }
}

const embed_mode = true;
const clear = document.getElementById('clearBtnId');
const clearContainer = get('.clear-btn-container');
const mainArea = get('.msger');
const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

// Constants for bot and person details
const BOT_IMG = "https://static.thenounproject.com/png/2216285-200.png";
const PERSON_IMG = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1024px-Default_pfp.svg.png";
const BOT_NAME = "ChatTutor";
const PERSON_NAME = "Student";

// URLs for production and debugging
const prodAskURL = new URL("https://chattutor-393319.ue.r.appspot.com/ask");
const debugAskURL = new URL("http://127.0.0.1:5000/ask");

// Variables to hold conversation and message details
var conversation = [];
var original_file = "";
let lastMessageId = null;
var stopGeneration = false

// Get the send button
const sendBtn = document.getElementById('sendBtn');
const themeBtn = document.getElementById('themeBtn')
const minimizeBtn = document.getElementById('minimizeBtn')
const themeBtnDiv = document.getElementById('themeBtnDiv')
const messageInput = document.getElementById('msgInput')
const scrollHelper = document.getElementById('scrollHelper')
const stopGenButton = document.getElementById('stopBtnId')

messageInput.addEventListener('input', (event) => {
  console.log('kajk')
  sendBtn.disabled = messageInput.value.length === 0;
})

stopGenButton.style.display = 'none'
// Listen for windoe resize to move the 'theme toggle button
window.addEventListener('resize', windowIsResizing)

function windowIsResizing() {
    // the button for choosing themes snaps in place when the window is too small
  if(true) {
      themeBtnDiv.style.position = 'inherit'
      themeBtnDiv.style.top = '25px'
      themeBtnDiv.style.left = '25px'

      const arr = [themeBtn, minimizeBtn]
      arr.forEach(btn => {
        btn.style.backgroundColor = 'transparent'
        btn.style.color = 'var(--msg-header-txt)'
        btn.style.textDecoration = 'underline'
        btn.style.padding = '0'
        btn.style.boxShadow = 'none'
        btn.style.border = 'none'
        btn.style.borderRadius = '0px'
        btn.style.margin = '0'

        btn.style.height = 'unset'
        btn.style.width = 'unset'
      })

  } else {
      themeBtnDiv.style.position = 'fixed'
      themeBtnDiv.style.top = '25px'
      themeBtnDiv.style.left = '25px'
      const arr = [themeBtn, minimizeBtn]
      arr.forEach(btn => {
        btn.style.backgroundColor = 'rgb(140, 0, 255)'
        btn.style.color = 'white'
        btn.style.textDecoration = 'none'
        btn.style.padding = '10px'
        btn.style.boxShadow = '0 5px 5px -5px rgba(0, 0, 0, 0.2)'
        btn.style.border = 'var(--border)'
        btn.style.borderRadius = '50%'
        btn.style.margin = '0'
        btn.style.height = '40px'
        btn.style.width = '40px'
      })
  }
}

function getFormattedIntegerFromDate() {
    let d = Date.now()

}

const smallCard = {
  card_max_width: '867px'
}

const bigCard = {
  card_max_width: 'unset'
}

let theme = null
let interfaceTheme = null

// Configures UI
if(embed_mode) {
  setupEmbedMode();
}

function uploadMessageToDB(msg, chat_k) {
    // NOT YET IMPLEMENTED HERE. NEED PR FOR MESSAGE DB IN MAIN REPO
}

// Event listener to clear conversation
clear.addEventListener('click', clearConversation);

// Event listener to handle form submission
msgerForm.addEventListener("submit", handleFormSubmit);

// Event listener to load conversation from local storage on DOM load
document.addEventListener("DOMContentLoaded", loadConversationFromLocalStorage);


document.addEventListener('DOMContentLoaded', setThemeOnRefresh)

document.addEventListener('DOMContentLoaded', windowIsResizing)

// Event listener for toggling the theme
themeBtn.addEventListener('click', toggleDarkMode)

stopGenButton.addEventListener('click', stopGenerating)

// I dodn't know if i should install uuidv4 using npm or what should i use
function uuidv4() {
  return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

function setChatId() {
    localStorage.setItem('conversation_id', uuidv4())
}

function getChatId() {
    return localStorage.getItem('conversation_id')
}

function setRefreshableChatId() {
    localStorage.setItem('conversation_r_id', uuidv4())
}

function removeRefreshableChatId() {
    localStorage.removeItem('conversation_r_id')
}

function getRefreshableChatId() {
    return localStorage.getItem('conversation_r_id')
}

function increaseClearNumber() {
    let clnr = getClearNumber()
    let clear_number = parseInt(clnr)
    localStorage.setItem('clear_number', `${clear_number+1}`)
}

function resetClearNumber() {
    localStorage.setItem('clear_number', '0')
}

function getClearNumber() {
    return localStorage.getItem('clear_number')
}

function reinstantiateChatId() {
    increaseClearNumber()
}

// function for keeping the theme whn the page refreshes
function setThemeOnRefresh() {
  // disable send button
  sendBtn.disabled = messageInput.value.length === 0;
  if(getChatId() == null) {
    setChatId()
  }
  removeRefreshableChatId()
  if(getRefreshableChatId() == null) {
    setRefreshableChatId()
  }

  if(getClearNumber() == null) {
      resetClearNumber()
  }

  theme = localStorage.getItem('theme')
  if (theme == null) {
    setTheme('dark')
  } else {
    setTheme(theme)
  }

  interfaceTheme = 'normal'
  setTheme('normal')

}
// helper function
function setTheme(th) {
  setProperties()
  const _style = "\"font-size: 15px !important; padding: 0 !important; margin: 0 !important; vertical-align: middle\""
    themeBtn.innerHTML = theme === "dark" ? `<span class="material-symbols-outlined" style=${_style}> light_mode </span>` :
        `<i class="material-symbols-outlined" style=${_style}> dark_mode\n </i>`
}

// function that toggles theme
function toggleDarkMode() {
  if (theme === 'light') {
    theme = 'dark'
  } else if(theme === 'dark') {
    theme = 'light'
  } else {
    theme = 'dark'
  }
  localStorage.setItem('theme', theme)
  setTheme(theme)
}

function toggleInterfaceMode() {
  interfaceTheme = 'normal'
  localStorage.setItem('interfacetheme', interfaceTheme)
  setTheme(interfaceTheme)

}

function clearConversation() {
  conversation = [];
  localStorage.setItem("conversation", JSON.stringify([]));
    reinstantiateChatId()
  var childNodes = msgerChat.childNodes;
  for(var i = childNodes.length - 3; i >= 2; i--){
      var childNode = childNodes[i];
      if (childNode.id !== 'clearContId' && childNode.id !== 'clearBtnId') {
        childNode.parentNode.removeChild(childNode);
      }
  }
  sendBtn.disabled = false;
}

function stopGenerating() {
  stopGeneration = true
}

function handleFormSubmit(event) {
  event.preventDefault();
  const msgText = msgerInput.value;
  if (!msgText) return;

  // Disable the send button
  sendBtn.disabled = true;
  clear.style.display = 'none'
  stopGenButton.style.display = 'flex'

  addMessage("user", msgText, true);
  uploadMessageToDB({role: 'user', content: msgText}, getChatId())
  msgerInput.value = "";
  queryGPT();
}


function loadConversationFromLocalStorage() {
  conversation = JSON.parse(localStorage.getItem("conversation"))
  if(conversation){
    conversation.forEach(message => {addMessage(message["role"], message["content"], false)})
  }
  else conversation = []
  //MathJax.typesetPromise();
}




function queryGPT() {
  const args = {
    "conversation": conversation,
    "collection": "MIT62410lab"
  }
  // if (embed_mode) args.from_doc = original_file
    url = new URL('https://chattutor-git-nbqjgewnea-uc.a.run.app/ask')
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(args)
  }).then(response => {
    const reader = response.body.getReader();
    let accumulatedContent = "";
    let isFirstMessage = true;
    function read() {
      reader.read().then(({ done, value }) => {
        if (done) {
          // Enable the send button when streaming is done
          sendBtn.disabled = false;
          clear.style.display = 'flex'
          stopGenButton.style.display = 'none'
          stopGeneration = false
            uploadMessageToDB({content: accumulatedContent, role: 'assistant'}, getChatId())
          return;
        }
        const strValue = new TextDecoder().decode(value);
        const messages = strValue.split('\n\n').filter(Boolean).map(chunk => JSON.parse(chunk.split('data: ')[1]));
          let message;
          for (var messageIndex in messages) {
              message = messages[messageIndex]
              if (stopGeneration === false) {
                  const contentToAppend = message.message.content ? message.message.content : "";
                  accumulatedContent += contentToAppend;
              }
              if (isFirstMessage) {
                  addMessage("assistant", accumulatedContent, false);
                  isFirstMessage = false;
              } else {
                  if (typeof (message.message.content) == 'undefined') {
                      conversation.push({"role": 'assistant', "content": accumulatedContent})
                      localStorage.setItem("conversation", JSON.stringify(conversation))
                  }
                  scrollHelper.scrollIntoView()
                  updateLastMessage(accumulatedContent);
              }
              if (stopGeneration === true) {
                  accumulatedContent += " ...Stopped generating";
                  conversation.push({"role": 'assistant', "content": accumulatedContent})
                  localStorage.setItem("conversation", JSON.stringify(conversation))
                  sendBtn.disabled = false;
                  clear.style.display = 'flex'
                  stopGenButton.style.display = 'none'
                  uploadMessageToDB({content: accumulatedContent, role: 'assistant'}, getChatId())
                  scrollHelper.scrollIntoView()
                  updateLastMessage(accumulatedContent);
                  break
              }
          }
        if(stopGeneration === false) {
          read();
        } else {
          stopGeneration = false
        }
      }).catch(err => {
        console.error('Stream error:', err);
        sendBtn.disabled = false;
        clear.style.display = 'flex'
        stopGenButton.style.display = 'none'
        stopGeneration = false
      });
    }
    read();
  }).catch(err => {
    console.error('Fetch error:', err);
    // Enable the send button in case of an error
    sendBtn.disabled = false;
    clear.style.display = 'flex'
    stopGenButton.style.display = 'none'
    stopGeneration = false
  });
}
// function queryGPT() {
//   args = {
//     "conversation": conversation,
//     "collection": "test_embedding"
//   }
//   if (embed_mode) args.from_doc = original_file
//   console.log("request:", JSON.stringify(args))
//   fetch(`${window.location.origin}/ask`, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-Accel-Buffering': 'no'
//     },
//     body: JSON.stringify(args)
//   }).then(response => {
//     console.log("responded")
//     const reader = response.body.getReader();
//     let accumulatedContent = "";
//     let isFirstMessage = true;
//     function read() {
//       console.log("reading...")
//       console.error("reading....");

//       reader.read().then(({ done, value }) => {
//         if (done) {
//           // Enable the send button when streaming is done
//             sendBtn.disabled = false;
//             clear.style.display = 'block'
//             stopGenButton.style.display = 'none'
//             stopGeneration = false
//             uploadMessageToDB({content: accumulatedContent, role: 'assistant'}, getChatId())
//           return;
//         }
//         const strValue = new TextDecoder().decode(value);
//         console.log(strValue.split('\n[CHUNK]\n').filter(Boolean))
//         const messages = strValue.split('\n[CHUNK]\n').filter(Boolean).map(chunk => {
//           try {
//             return JSON.parse(chunk.split('data: ')[1])
//           } catch(e) {
//             return {'time': 0, 'message': ''}
//           }
//         });
//         console.log(messages)
//         messages.forEach(message => {
//           const contentToAppend = message.message.content ? message.message.content : "";
//           accumulatedContent += contentToAppend;
//           console.log(accumulatedContent)
//           console.error(accumulatedContent);


//           if(stopGeneration === false) {
//             const contentToAppend = message.message.content ? message.message.content : "";
//             accumulatedContent += contentToAppend;
//           }
//           if (isFirstMessage) {
//             addMessage("assistant", accumulatedContent, false);
//             isFirstMessage = false;
//           } else {
//             if (typeof (message.message.content) == 'undefined') {
//               conversation.push({"role": 'assistant', "content": accumulatedContent})
//               localStorage.setItem("conversation", JSON.stringify(conversation))
//             }
//             scrollHelper.scrollIntoView()
//             updateLastMessage(accumulatedContent);
//           }

//           if(stopGeneration === true) {
//               accumulatedContent += " ...Stopped generating";
//               conversation.push({"role": 'assistant', "content": accumulatedContent})
//               localStorage.setItem("conversation", JSON.stringify(conversation))

//               sendBtn.disabled = false;
//               clear.style.display = 'block'
//               stopGenButton.style.display = 'none'
//               scrollHelper.scrollIntoView()
//               updateLastMessage(accumulatedContent);
//               uploadMessageToDB({content: accumulatedContent, role: 'assistant'}, getChatId())
//               return;
//           }
//         })
//         if(stopGeneration === false) {
//           read();
//         } else {
//           stopGeneration = false
//         }
//       }).catch(err => {
//         console.error('Stream error:', err);
//         sendBtn.disabled = false;
//         clear.style.display = 'block'
//         stopGenButton.style.display = 'none'
//         stopGeneration = false
//       });
//     }
//     read();
//   }).catch(err => {
//     console.error('Fetch error:', err);
//     // Enable the send button in case of an error
//     sendBtn.disabled = false;
//     clear.style.display = 'block'
//     stopGenButton.style.display = 'none'
//     stopGeneration = false
//   });
// }

function formatMessage(message, makeLists = true) {
  const messageArr = message.split("\n")

  let messageStr = ""
  let listSwitch = 0
  for (let messageArrIndex in messageArr) {
    const paragraph = messageArr[messageArrIndex]
    if(paragraph.startsWith('- ') && makeLists) {
      if(listSwitch === 0) {
        messageStr += "<ul style=\"padding-left: 15px !important; color: var(--left-msg-txt)\">"
      }

      messageStr += `<li><p style="color: var(--left-msg-txt)">${paragraph.slice(2)}</p></li>`

      listSwitch = 1

    } else if (listSwitch === 1) {
      messageStr += "</ul>"
      messageStr += `<p style="color: var(--left-msg-txt)">${paragraph}</p>`
      listSwitch = 0
    } else {
      messageStr += `<p style="color: var(--left-msg-txt)">${paragraph}</p>`
      listSwitch = 0
    }

  }
  return messageStr
}

function updateLastMessage(newContent) {
  if (lastMessageId) {
    const lastMessageElement = document.querySelector(`#${lastMessageId} .msg-text`);
    if (lastMessageElement) {
      const newContentFormatted = formatMessage(newContent)
      document.querySelector(`#${lastMessageId} .msg-text`).innerHTML = newContentFormatted;
    } else {
      console.error('Cannot find the .msg-text element to update.');
    }
  } else {
    console.error('No message has been added yet.');
  }
  //MathJax.typesetPromise();

}




function addMessage(role, message, updateConversation) {
    let role_name
    let img
    let side
  if(role === "assistant") {
    role_name = BOT_NAME;
    img = BOT_IMG;
    side = "left";

  }
  else {
    role_name = PERSON_NAME;
    img = PERSON_IMG;
    side = "right";
  }

  const messageId = 'msg-' + new Date().getTime();
  lastMessageId = messageId;

  // if you want to make the robot white ( of course it doesn't work well in safari ), so -- not in use right now
  var invertImage = 'invert(0%)'
  if (side === "left") {
    invertImage = 'var(--msg-invert-image)'
  }

  const messageStr = formatMessage(message, role === "assistant")

  const msgHTML = `
    <div class="msg ${side}-msg" id="${messageId}">
    <div class="msg-bgd">

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${role_name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${messageStr}</div>
      </div>
      </div>
    </div>
  `;

  clearContainer.insertAdjacentHTML("beforebegin", msgHTML);

  // Find the newly added message and animate it
  const newMessage = document.getElementById(messageId);
  newMessage.style.opacity = "0";
  newMessage.style.transform = "translateY(1rem)";
  
  // Trigger reflow to make the transition work
  void newMessage.offsetWidth;
  
  // Start the animation
  newMessage.style.opacity = "1";
  newMessage.style.transform = "translateY(0)";
  msgerChat.scrollTop += 500;
  if(updateConversation){
    conversation.push({"role": role, "content": message})
    localStorage.setItem("conversation", JSON.stringify(conversation))
  }
}


function setupEmbedMode() {
  // Setup minimize and expand buttons to toggle 'minimized' class on mainArea
  const minimize = get('.msger-minimize');
  const expand = get('.msger-expand');
  minimize.addEventListener('click', () => mainArea.classList.toggle('minimized'));
  expand.addEventListener('click', () => mainArea.classList.toggle('minimized'));

  // Extract and store the name of the original file from the 'Download source file' link
  const download_original = document.querySelectorAll('[title="Download source file"]')[0];
  original_file = download_original.getAttribute("href").slice(download_original.getAttribute("href").lastIndexOf("/") + 1);
}


// Utility functions
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}
