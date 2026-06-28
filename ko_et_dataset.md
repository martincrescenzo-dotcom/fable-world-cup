# KO Extra-Time dataset — calibration source for `ko_build.py` (ρ, φ)

**STATUS: integrity-checked (internal consistency PASS), aggregate recounted programmatically by
`ko_build.py` (it reads ρ from these rows directly — no hand-entered totals).** Assembled by 4
web-research subagents reading Wikipedia knockout-stage pages. Post-2004 only (no golden-goal regime).
Senior men's international major tournaments. **Caveat: rows pass INTERNAL consistency but are NOT
independently verified vs source** — a row could have wrong-but-self-consistent scores. The Euro
subagent's summary miscounted pens (said 12, table has 14); aggregate is now counted from rows, not
summaries. Watch the Copa/AFCON "straight-to-pens, no ET played" exclusions.

Aggregate used in calibration: **N=132 ET matches, 86 went to pens (stayed level through 120').
rho = 86/132 = 0.652.** ET-goal totals hand-tallied to: {0:82, 1:37, 2:10, 3:2, 4:1}, mean 0.508.

Columns: Tournament | Year | Round | TeamA | TeamB | Score@90 | Score@120(excl pens) | Pens(Y/N) | Conf

## World Cup 2006–2022 (28 ET, 19 pens)
| WC | 2006 | R16 | Argentina | Mexico | 1-1 | 2-1 | N | High |
| WC | 2006 | R16 | Switzerland | Ukraine | 0-0 | 0-0 | Y | High |
| WC | 2006 | QF | Germany | Argentina | 1-1 | 1-1 | Y | High |
| WC | 2006 | QF | England | Portugal | 0-0 | 0-0 | Y | High |
| WC | 2006 | SF | Germany | Italy | 0-0 | 0-2 | N | High |
| WC | 2006 | Final | Italy | France | 1-1 | 1-1 | Y | High |
| WC | 2010 | R16 | USA | Ghana | 1-1 | 1-2 | N | High |
| WC | 2010 | R16 | Paraguay | Japan | 0-0 | 0-0 | Y | High |
| WC | 2010 | QF | Uruguay | Ghana | 1-1 | 1-1 | Y | High |
| WC | 2010 | Final | Netherlands | Spain | 0-0 | 0-1 | N | High |
| WC | 2014 | R16 | Brazil | Chile | 1-1 | 1-1 | Y | High |
| WC | 2014 | R16 | Costa Rica | Greece | 1-1 | 1-1 | Y | High |
| WC | 2014 | R16 | Germany | Algeria | 0-0 | 2-1 | N | High |
| WC | 2014 | R16 | Argentina | Switzerland | 0-0 | 1-0 | N | High |
| WC | 2014 | R16 | Belgium | USA | 0-0 | 2-1 | N | High |
| WC | 2014 | QF | Netherlands | Costa Rica | 0-0 | 0-0 | Y | High |
| WC | 2014 | SF | Netherlands | Argentina | 0-0 | 0-0 | Y | High |
| WC | 2014 | Final | Germany | Argentina | 0-0 | 1-0 | N | High |
| WC | 2018 | R16 | Spain | Russia | 1-1 | 1-1 | Y | High |
| WC | 2018 | R16 | Croatia | Denmark | 1-1 | 1-1 | Y | High |
| WC | 2018 | R16 | Colombia | England | 1-1 | 1-1 | Y | High |
| WC | 2018 | QF | Russia | Croatia | 2-2 | 2-2 | Y | High |
| WC | 2018 | SF | Croatia | England | 1-1 | 2-1 | N | High |
| WC | 2022 | R16 | Japan | Croatia | 1-1 | 1-1 | Y | High |
| WC | 2022 | R16 | Morocco | Spain | 0-0 | 0-0 | Y | High |
| WC | 2022 | QF | Croatia | Brazil | 0-0 | 1-1 | Y | High |
| WC | 2022 | QF | Netherlands | Argentina | 2-2 | 2-2 | Y | High |
| WC | 2022 | Final | Argentina | France | 2-2 | 3-3 | Y | High |

## Euro 2008-2024 (23 ET, 14 pens)
| Euro | 2008 | QF | Croatia | Turkey | 0-0 | 1-1 | Y | High |
| Euro | 2008 | QF | Netherlands | Russia | 1-1 | 1-3 | N | High |
| Euro | 2008 | QF | Spain | Italy | 0-0 | 0-0 | Y | High |
| Euro | 2012 | QF | England | Italy | 0-0 | 0-0 | Y | High |
| Euro | 2012 | SF | Portugal | Spain | 0-0 | 0-0 | Y | High |
| Euro | 2016 | R16 | Switzerland | Poland | 1-1 | 1-1 | Y | High |
| Euro | 2016 | R16 | Croatia | Portugal | 0-0 | 0-1 | N | High |
| Euro | 2016 | QF | Poland | Portugal | 1-1 | 1-1 | Y | High |
| Euro | 2016 | QF | Germany | Italy | 1-1 | 1-1 | Y | High |
| Euro | 2016 | Final | Portugal | France | 0-0 | 1-0 | N | High |
| Euro | 2020 | R16 | Italy | Austria | 1-1 | 2-1 | N | High |
| Euro | 2020 | R16 | Croatia | Spain | 3-3 | 3-5 | N | High |
| Euro | 2020 | R16 | France | Switzerland | 3-3 | 3-3 | Y | High |
| Euro | 2020 | R16 | Sweden | Ukraine | 1-1 | 1-2 | N | High |
| Euro | 2020 | QF | Switzerland | Spain | 1-1 | 1-1 | Y | High |
| Euro | 2020 | SF | Italy | Spain | 1-1 | 1-1 | Y | High |
| Euro | 2020 | SF | England | Denmark | 1-1 | 2-1 | N | High |
| Euro | 2020 | Final | Italy | England | 1-1 | 1-1 | Y | High |
| Euro | 2024 | R16 | England | Slovakia | 1-1 | 2-1 | N | High |
| Euro | 2024 | R16 | Portugal | Slovenia | 0-0 | 0-0 | Y | High |
| Euro | 2024 | QF | Spain | Germany | 1-1 | 2-1 | N | High |
| Euro | 2024 | QF | Portugal | France | 0-0 | 0-0 | Y | High |
| Euro | 2024 | QF | England | Switzerland | 1-1 | 1-1 | Y | High |

## Copa América + Confederations Cup (12 ET, 8 pens)
NOTE: many Copa KO matches went STRAIGHT to pens with no ET (2007, and all non-final rounds in
2015/2016/2019/2021/2024) — those are EXCLUDED here. Only ET-played matches below.
| Copa | 2011 | QF | Colombia | Peru | 0-0 | 0-2 | N | High |
| Copa | 2011 | QF | Argentina | Uruguay | 1-1 | 1-1 | Y | High |
| Copa | 2011 | QF | Brazil | Paraguay | 0-0 | 0-0 | Y | High |
| Copa | 2011 | SF | Paraguay | Venezuela | 0-0 | 0-0 | Y | High |
| Copa | 2015 | Final | Chile | Argentina | 0-0 | 0-0 | Y | High |
| Copa | 2016 | Final | Argentina | Chile | 0-0 | 0-0 | Y | High |
| Copa | 2024 | Final | Argentina | Colombia | 0-0 | 1-0 | N | High |
| Confed | 2009 | 3rd | Spain | South Africa | 2-2 | 3-2 | N | High |
| Confed | 2013 | SF | Spain | Italy | 0-0 | 0-0 | Y | High |
| Confed | 2013 | 3rd | Italy | Uruguay | 2-2 | 2-2 | Y | High |
| Confed | 2017 | SF | Portugal | Chile | 0-0 | 0-0 | Y | High |
| Confed | 2017 | 3rd | Portugal | Mexico | 1-1 | 2-1 | N | High |

## AFCON + Asian Cup + Gold Cup (69 ET, 45 pens)
| AFCON | 2006 | QF | Nigeria | Tunisia | 1-1 | 1-1 | Y | High |
| AFCON | 2006 | QF | Cameroon | Ivory Coast | 1-1 | 1-1 | Y | High |
| AFCON | 2006 | Final | Egypt | Ivory Coast | 0-0 | 0-0 | Y | High |
| AFCON | 2008 | QF | Tunisia | Cameroon | 2-2 | 2-3 | N | High |
| AFCON | 2010 | QF | Ivory Coast | Algeria | 2-2 | 2-3 | N | High |
| AFCON | 2010 | QF | Egypt | Cameroon | 1-1 | 3-1 | N | High |
| AFCON | 2010 | QF | Zambia | Nigeria | 0-0 | 0-0 | Y | High |
| AFCON | 2012 | QF | Gabon | Mali | 1-1 | 1-1 | Y | High |
| AFCON | 2012 | QF | Ghana | Tunisia | 1-1 | 2-1 | N | High |
| AFCON | 2012 | Final | Zambia | Ivory Coast | 0-0 | 0-0 | Y | High |
| AFCON | 2013 | QF | South Africa | Mali | 1-1 | 1-1 | Y | High |
| AFCON | 2013 | QF | Burkina Faso | Togo | 0-0 | 1-0 | N | High |
| AFCON | 2013 | SF | Burkina Faso | Ghana | 1-1 | 1-1 | Y | High |
| AFCON | 2015 | QF | Tunisia | Equatorial Guinea | 1-1 | 1-2 | N | High |
| AFCON | 2015 | Final | Ivory Coast | Ghana | 0-0 | 0-0 | Y | High |
| AFCON | 2017 | QF | Senegal | Cameroon | 0-0 | 0-0 | Y | High |
| AFCON | 2017 | SF | Burkina Faso | Egypt | 1-1 | 1-1 | Y | High |
| AFCON | 2019 | R16 | Morocco | Benin | 1-1 | 1-1 | Y | High |
| AFCON | 2019 | R16 | Madagascar | DR Congo | 2-2 | 2-2 | Y | High |
| AFCON | 2019 | R16 | Ghana | Tunisia | 1-1 | 1-1 | Y | High |
| AFCON | 2019 | QF | Ivory Coast | Algeria | 1-1 | 1-1 | Y | High |
| AFCON | 2019 | SF | Senegal | Tunisia | 0-0 | 1-0 | N | High |
| AFCON | 2021 | R16 | Burkina Faso | Gabon | 1-1 | 1-1 | Y | High |
| AFCON | 2021 | R16 | Ivory Coast | Egypt | 0-0 | 0-0 | Y | High |
| AFCON | 2021 | R16 | Mali | Equatorial Guinea | 0-0 | 0-0 | Y | High |
| AFCON | 2021 | QF | Egypt | Morocco | 1-1 | 2-1 | N | High |
| AFCON | 2021 | SF | Cameroon | Egypt | 0-0 | 0-0 | Y | High |
| AFCON | 2021 | Final | Senegal | Egypt | 0-0 | 0-0 | Y | High |
| AFCON | 2023 | R16 | Egypt | DR Congo | 1-1 | 1-1 | Y | High |
| AFCON | 2023 | R16 | Senegal | Ivory Coast | 1-1 | 1-1 | Y | High |
| AFCON | 2023 | QF | Mali | Ivory Coast | 1-1 | 1-2 | N | High |
| AFCON | 2023 | QF | Cape Verde | South Africa | 0-0 | 0-0 | Y | High |
| AFCON | 2023 | SF | Nigeria | South Africa | 1-1 | 1-1 | Y | High |
| Asian | 2007 | QF | Japan | Australia | 1-1 | 1-1 | Y | High |
| Asian | 2007 | QF | Iran | South Korea | 0-0 | 0-0 | Y | High |
| Asian | 2007 | SF | Iraq | South Korea | 0-0 | 0-0 | Y | High |
| Asian | 2007 | 3rd | South Korea | Japan | 0-0 | 0-0 | Y | High |
| Asian | 2011 | QF | Australia | Iraq | 0-0 | 1-0 | N | High |
| Asian | 2011 | QF | South Korea | Iran | 0-0 | 1-0 | N | High |
| Asian | 2011 | SF | Japan | South Korea | 2-2 | 2-2 | Y | High |
| Asian | 2011 | Final | Japan | Australia | 0-0 | 1-0 | N | High |
| Asian | 2015 | QF | South Korea | Uzbekistan | 0-0 | 2-0 | N | High |
| Asian | 2015 | QF | Iran | Iraq | 1-1 | 3-3 | Y | High |
| Asian | 2015 | QF | Japan | UAE | 1-1 | 1-1 | Y | High |
| Asian | 2015 | Final | Australia | South Korea | 1-1 | 2-1 | N | High |
| Asian | 2019 | R16 | Jordan | Vietnam | 1-1 | 1-1 | Y | High |
| Asian | 2019 | R16 | Australia | Uzbekistan | 0-0 | 0-0 | Y | High |
| Asian | 2019 | R16 | UAE | Kyrgyzstan | 2-2 | 3-2 | N | High |
| Asian | 2019 | R16 | South Korea | Bahrain | 1-1 | 2-1 | N | High |
| Asian | 2023 | R16 | Tajikistan | UAE | 1-1 | 1-1 | Y | High |
| Asian | 2023 | R16 | Saudi Arabia | South Korea | 1-1 | 1-1 | Y | High |
| Asian | 2023 | R16 | Iran | Syria | 1-1 | 1-1 | Y | High |
| Asian | 2023 | QF | Australia | South Korea | 1-1 | 1-2 | N | High |
| Asian | 2023 | QF | Qatar | Uzbekistan | 1-1 | 1-1 | Y | High |
| Gold | 2007 | QF | Mexico | Costa Rica | 0-0 | 1-0 | N | High |
| Gold | 2009 | QF | United States | Panama | 1-1 | 2-1 | N | High |
| Gold | 2009 | SF | Costa Rica | Mexico | 1-1 | 1-1 | Y | High |
| Gold | 2011 | QF | Costa Rica | Honduras | 1-1 | 1-1 | Y | High |
| Gold | 2011 | QF | Panama | El Salvador | 1-1 | 1-1 | Y | High |
| Gold | 2011 | SF | Honduras | Mexico | 0-0 | 0-2 | N | High |
| Gold | 2015 | QF | Trinidad and Tobago | Panama | 1-1 | 1-1 | Y | High |
| Gold | 2015 | QF | Mexico | Costa Rica | 0-0 | 1-0 | N | High |
| Gold | 2015 | SF | Mexico | Panama | 1-1 | 2-1 | N | High |
| Gold | 2015 | 3rd | Panama | United States | 1-1 | 1-1 | Y | High |
| Gold | 2019 | QF | Mexico | Costa Rica | 1-1 | 1-1 | Y | High |
| Gold | 2019 | SF | Haiti | Mexico | 0-0 | 0-1 | N | High |
| Gold | 2021 | Final | United States | Mexico | 0-0 | 1-0 | N | High |
| Gold | 2023 | QF | United States | Canada | 2-2 | 2-2 | Y | High |
| Gold | 2023 | SF | United States | Panama | 1-1 | 1-1 | Y | High |
