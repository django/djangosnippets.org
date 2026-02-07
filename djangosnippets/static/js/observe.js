const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.5,
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.start();
        }
    })
}, observerOptions);

export default observer;
