const videoContainer = document.getElementById('video-container');
const video = document.getElementById('my-video');

// Xử lý sự kiện khi bật/tắt chế độ rạp chiếu phim
video.addEventListener('fullscreenchange', handleFullscreenChange);
video.addEventListener('mozfullscreenchange', handleFullscreenChange);
video.addEventListener('webkitfullscreenchange', handleFullscreenChange);

function handleFullscreenChange() {
    if (isFullscreen()) {
        videoContainer.classList.add('video-fullscreen');
    } else {
        videoContainer.classList.remove('video-fullscreen');
    }
}

function isFullscreen() {
    return !!(document.fullscreenElement || document.mozFullScreenElement || document.webkitFullscreenElement);
}

// Xử lý sự kiện cuộn trang web khi ở chế độ rạp chiếu phim
videoContainer.addEventListener('scroll', function (event) {
    if (isFullscreen()) {
        event.preventDefault();
    }
});
