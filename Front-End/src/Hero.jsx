import { useEffect, useRef } from "react"
import gsap from "gsap"

import { ScrollTrigger } from "gsap/ScrollTrigger"
gsap.registerPlugin(ScrollTrigger)

import logo from "./assets/Logo.png"
import bg from "./assets/BG.png"

export default function Hero() {
  const textRef = useRef(null)
  const logoRef = useRef(null)

  useEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ".parent",
          start: "top 80%",
          end: "bottom 20%",
          toggleActions: "play reverse play reverse",
        },
        defaults: {
          ease: "power3.out",
        },
      })

      tl.from(
        textRef.current, {
        opacity: 0,
        y: 60,
        duration: 1,
      }),

        tl.from(
          logoRef.current,
          {
            opacity: 0,
            x: +60,
            duration: 1,
          },
          "-=0.5"
        )

    })

    return () => ctx.revert()
  }, [])

  return (
    <section className="parent">
      {/* TEXT */}
      <div className="div1" ref={textRef}>
        <h1 className="megrim-regular">
          Sentinel <span>AI</span>
        </h1>
        <p className="gruppo-regular">
          AI Powered Cyber-Security Dashboard
        </p>
      </div>

      {/* LOGO STACK */}
      <div className="div2">
        <div className="logo-stack" ref={logoRef}>
          <img src={bg} alt="" className="logo-bg" />
          <img
            src={logo}
            alt="Sentinel AI Logo"
            className="logo-fg"
          />
        </div>
      </div>
    </section>
  )
}
