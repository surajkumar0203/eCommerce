const trackIdRef = document.getElementById('track-id')
const trackId=trackIdRef.innerText.trim()

// Create WebSocket connection.
const socket = new WebSocket(`ws://127.0.0.1:8000/ws/order/${trackId}/`);

// on receiving message
socket.onmessage = (event) => {
  
    const data= JSON.parse(event.data);
    
    let progress_percentage=data.payload.progress_percentage
    let status=data.payload.status
   
    changeInUI(progress_percentage,status)
}

const changeInUI = (progress_percentage,status) =>{
    const progressRef=document.querySelector('.progress-bar');
    const statusRef=document.querySelector('#show_order_status');
    statusRef.innerText = `Status : ${status}`
    if(progress_percentage===100){
        progressRef.classList.add('bg-success')
    }
    progressRef.innerText = `${progress_percentage}%`
    progressRef.style.width=`${progress_percentage}%`
}