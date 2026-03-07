import { useRef, useLayoutEffect } from "react"
import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"
import aboutImg from "./assets/About.png"

gsap.registerPlugin(ScrollTrigger)

export default function About() {
  const titleRef = useRef(null)
  const imgRef = useRef(null)
  const textRef = useRef(null)

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: "#Aboutus",
          start: "top 75%",
          end: "bottom 30%",
          toggleActions: "play reverse play reverse",
        },
        defaults: {
          ease: "power3.out",
        },
      })

      // 1️⃣ Title fades in first
      tl.from(titleRef.current, {
        opacity: 0,
        y: 30,
        duration: 0.6,
      })

      // 2️⃣ Image + text fade in together from opposite sides
      tl.from(
        imgRef.current,
        {
          opacity: 0,
          x: -60,
          duration: 1,
        },
        "+=0.1"
      )

      tl.from(
        textRef.current,
        {
          opacity: 0,
          x: 60,
          duration: 0.8,
        },
        "<" 
      )
    })

    return () => ctx.revert()
  }, [])

  return (
    <>
      <div className="AboutTitle" ref={titleRef}>
        <h1>
          <span>What</span> Is Sentinel <span>?</span>
        </h1>
      </div>

      <section className="Aboutus" id="Aboutus">
        <div className="div2" ref={imgRef}>
          <img src={aboutImg} alt="About" />
        </div>

        <div className="div1" ref={textRef}>
          <p>
            Dot Sentinel Al is an innovative cybersecurity dashboard designed to
            simplify the analysis of PCAP log files using agentic AI, enabling
            rapid detection of network threats like malware, unauthorized access,
            or anomalies. It autonomously processes complex packet data,
            generating clear, user-friendly reports with intuitive
            visualizations that cater to both technical and non-technical users.
          </p>
        </div>
      </section>
    </>
  )
}
