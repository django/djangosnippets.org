import observer from './observe.js';


class TypingAnimation {
    /**
    * @param {HTMLElement} element - It is an element with the attribute `data-animation="typing"`,
    *                                to which the typing effect is applied.
    * @param {string} word - Text to display with typing animation effect.
    * @param {Boolean} useObserve
    * @param {number} speed - Typing speed in milliseconds.
    */
    constructor(element, word, useObserve=false, speed = 80) {
        this.element = element;
        this.word = word;
        this.speed = speed;
        this.currentIndex = 0;
        this.element.start = () => this.start();
        if (!useObserve) this.start();
    }

    start() {
        if (this.currentIndex <= this.word.length) {
            this.currentText = this.word.substring(0, this.currentIndex);
            this.element.textContent = this.currentText;
            this.currentIndex++;
            setTimeout(() => this.start(), this.speed);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const typingElements = document.querySelectorAll('[data-animation="typing"]');
    typingElements.forEach((node) => {
        const typingText = node.dataset.typingText;
        const useObserve = new Boolean(node.dataset.useObserve);
        const newNode = new TypingAnimation(node, typingText, useObserve);
        if (useObserve) observer.observe(newNode.element);
    });
});
