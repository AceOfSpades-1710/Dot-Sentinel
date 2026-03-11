import { useRef, useState, useLayoutEffect } from "react"
import gsap from "gsap"
import { API_BASE_URL } from '../config';
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
        { opacity: 0, y: 60 },
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

    if (activeIndex === index) {
      tl.reverse()
      setActiveIndex(null)
      return
    }

    tl.clear()

    const clickedCard = cardRefs.current[index]
    const otherCards = cardRefs.current.filter((_, i) => i !== index)

    tl.to(otherCards, {
      opacity: 0,
      scale: 0.95,
      duration: 0.4,
    })

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
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleDrop = async e => {
    e.preventDefault()
    if (isUploading) return

    const file = e.dataTransfer.files[0]
    if (!file) return

    await uploadFile(file)
  }

  const handleFileSelect = async e => {
    if (isUploading) return

    const file = e.target.files[0]
    if (!file) return

    await uploadFile(file)
  }

  const uploadFile = async file => {
    if (!file.name.endsWith(".pcap") && !file.name.endsWith(".pcapng")) {
      setError("Please upload a .pcap or .pcapng file")
      return
    }

    setIsUploading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append("file", file)

    try {
      const targetURL =
        window.location.hostname === "localhost"
          ? "/analyze"
          : `${API_BASE_URL.replace(/\/$/, "")}/analyze`

      const response = await fetch(targetURL, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`Upload failed (${response.status}): ${text}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      console.error("Upload error:", err)
      setError(err.message || "Failed to upload file")
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div
      className="drop-inner"
      onDragOver={e => e.preventDefault()}
      onDrop={handleDrop}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        gap: "1rem",
        width: "100%",
        height: "100%",
        overflowY: "auto",
      }}
    >
      {!result && !isUploading && (
        <>
          <p style={{ fontSize: "1.2rem", fontWeight: "bold" }}>
            Drop PCAP File Here
          </p>

          <p>or</p>

          <input
            type="file"
            accept=".pcap,.pcapng"
            onChange={handleFileSelect}
            style={{ color: "white" }}
          />
        </>
      )}

      {isUploading && <p>Analyzing traffic patterns...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ width: "100%", textAlign: "left" }}>
          <h3>Analysis Complete</h3>

          <p>Total Flows: {result.total_flows}</p>
          <p>
            Campaigns Detected:{" "}
            {result.campaigns ? result.campaigns.length : 0}
          </p>

          {result.campaigns && result.campaigns.length > 0 && (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "1rem",
                marginTop: "1rem",
                maxHeight: "400px",
                overflowY: "auto",
              }}
            >
              {result.campaigns.map((campaign, idx) => (
                <div
                  key={idx}
                  style={{
                    padding: "1rem",
                    backgroundColor: "rgba(255,255,255,0.05)",
                    borderRadius: "8px",
                    border: "1px solid #444",
                  }}
                >
                  <h4
                    style={{
                      marginTop: 0,
                      color: "#4ade80",
                    }}
                  >
                    Campaign {campaign.campaign_id} (Flows:{" "}
                    {campaign.flows.length})
                  </h4>

                  {campaign.llm_explanation && (
                    <div
                      style={{
                        padding: "0.8rem",
                        backgroundColor: "rgba(0,0,0,0.3)",
                        borderRadius: "6px",
                        marginBottom: "1rem",
                        fontSize: "0.9rem",
                        lineHeight: "1.4",
                      }}
                    >
                      <strong style={{ color: "#a78bfa" }}>
                        AI SOC Analysis:
                      </strong>

                      <p
                        style={{
                          whiteSpace: "pre-wrap",
                          margin: "0.5rem 0 0 0",
                        }}
                      >
                        {campaign.llm_explanation}
                      </p>
                    </div>
                  )}

                  <details>
                    <summary
                      style={{
                        cursor: "pointer",
                        opacity: 0.8,
                        fontSize: "0.9em",
                      }}
                    >
                      View Flows
                    </summary>

                    <ul
                      style={{
                        margin: "0.5rem 0 0 0",
                        paddingLeft: "1.2rem",
                        fontSize: "0.85em",
                        opacity: 0.9,
                      }}
                    >
                      {campaign.flows.map((flow, fidx) => (
                        <li
                          key={fidx}
                          style={{ marginBottom: "0.4rem" }}
                        >
                          <span
                            style={{
                              color:
                                flow.attack_prob > 0.5
                                  ? "#f87171"
                                  : "#9ca3af",
                            }}
                          >
                            [{flow.attack_type}]
                          </span>{" "}
                          {flow.src_ip} → {flow.dst_ip}

                          <span
                            style={{
                              opacity: 0.5,
                              marginLeft: "0.5rem",
                            }}
                          >
                            (Bytes: {flow.bytes})
                          </span>
                        </li>
                      ))}
                    </ul>
                  </details>
                </div>
              ))}
            </div>
          )}

          <button
            onClick={() => setResult(null)}
            style={{
              marginTop: "1.5rem",
              padding: "0.6rem 1.2rem",
              cursor: "pointer",
              backgroundColor: "#3b82f6",
              color: "white",
              border: "none",
              borderRadius: "4px",
              fontWeight: "bold",
            }}
          >
            Analyze Another PCAP
          </button>
        </div>
      )}
    </div>
  )
}
