import { useRef, useState, useLayoutEffect } from "react"
import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

gsap.registerPlugin(ScrollTrigger)

export default function Services() {
  const cardRefs = useRef([])
  const dropRef = useRef(null)
  const tlRef = useRef(null)

  const [activeIndex, setActiveIndex] = useState(null)

  /* ===============================
     SCROLL FADE-IN / FADE-OUT
  =============================== */
  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      gsap.fromTo(
        cardRefs.current,
        {
          opacity: 0,
          y: 60,
        },
        {
          opacity: 1,
          y: 0,
          duration: 1,
          ease: "power2.out",
          stagger: 0.2,
          scrollTrigger: {
            trigger: ".card",
            start: "top 80%",
            end: "bottom 20%",
            toggleActions: "play reverse play reverse",
          },
        }
      )
    })

    return () => ctx.revert()
  }, [])

  /* ===============================
     CLICK ANIMATION (FOCUS CARD)
  =============================== */
  useLayoutEffect(() => {
    const tl = gsap.timeline({
      paused: true,
      defaults: { ease: "power2.inOut" },
    })

    tlRef.current = tl

    return () => tl.kill()
  }, [])

  const handleCardClick = index => {
    const tl = tlRef.current
    if (!tl) return

    // Reverse if clicking active card again
    if (activeIndex === index) {
      tl.reverse()
      setActiveIndex(null)
      return
    }

    tl.clear()

    const clickedCard = cardRefs.current[index]
    const otherCards = cardRefs.current.filter((_, i) => i !== index)

    // Fade other cards
    tl.to(otherCards, {
      opacity: 0,
      scale: 0.95,
      duration: 0.4,
    })

    // Move clicked card left
    const targetX =
      cardRefs.current[0].offsetLeft - clickedCard.offsetLeft

    tl.to(
      clickedCard,
      {
        x: targetX,
        duration: 0.5,
      },
      "<"
    )

    // Reveal drop zone
    tl.to(
      dropRef.current,
      {
        opacity: 1,
        scale: 1,
        pointerEvents: "auto",
        x: -40,
        duration: 0.5,
      },
      "-=0.2"
    )

    tl.play()
    setActiveIndex(index)
  }

  return (
    <section id="services" className="parent-services">
      {[
        <>Generate Report with <span>URL</span></>,
        <>Generate Report with <span>PCAP</span> file</>,
        <>Analyse Previous <span>Reports</span></>,
      ].map((title, i) => (
        <div
          key={i}
          className={`div${i + 1}-services`}
          ref={el => (cardRefs.current[i] = el)}
        >
          <Card
            title={title}
            onView={() => handleCardClick(i)}
            active={activeIndex === i}
          />
        </div>
      ))}

      <div className="drop-zone" ref={dropRef}>
        <DropZone />
      </div>
    </section>
  )
}

/* ===============================
   CARD
=============================== */
function Card({ title, onView, active }) {
  return (
    <article className="card">
      <section className="card__hero">
        <p className="card__job-title">{title}</p>
      </section>

      <footer className="card__footer">
        <button className="card__btn" onClick={onView}>
          {active ? "Nahhh" : "This One!"}
        </button>
      </footer>
    </article>
  )
}

/* ===============================
   DROP ZONE
=============================== */
function DropZone() {
  const handleDrop = e => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    alert(`Uploaded: ${file.name}`)
  }

  return (
    <div
      className="drop-inner"
      onDragOver={e => e.preventDefault()}
      onDrop={handleDrop}
    >
      <p>Drop File Here</p>
    </div>
  )
}
