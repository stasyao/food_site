class Header {
    constructor(counter) {
        this.counter = counter;
        this.api = api;
        this.counterNum = this.counter.textContent;
        this.plusCounter = this.plusCounter.bind(this);
        this.minusCounter = this.minusCounter.bind(this);
    }

    plusCounter  ()  {
        this.counterNum = ++this.counterNum;
        this.counter.textContent = this.counterNum;
        this.counter.removeAttribute("hidden");
    }
    minusCounter ()  {
        this.counterNum = --this.counterNum;
        if (this.counterNum > 0){
            this.counter.textContent = this.counterNum;
        } else {
            this.counter.textContent = this.counterNum;
            this.counter.setAttribute("hidden", "hidden");
            let elem = document.getElementById("list_download");
            elem.setAttribute("hidden", "hidden");
        }
    }
}
