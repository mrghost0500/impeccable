"""Peer sets and valuation-gap research per finalist (Nov 2026).

`universe_peers` are tickers already in the cached screener universe, so their
metrics come from the same source and date as the finalist. `external_peers` are
larger sector leaders outside the cached band; their metrics come from web search
of aggregator snapshots (dates noted) and are approximate.
"""

COMPS = {
 "SRM": dict(
  universe_peers=["PNCINFRA", "KNRCON", "HGINFRA", "JKIL", "GPTINFRA", "PSPPROJECT"],
  external_peers=[],
  competitors="The listed road-EPC incumbents are shrinking: 3Y sales CAGR is -10% at PNC Infratech, -14% at KNR and about flat at H.G. Infra, as NHAI awarding slowed and HAM receivables tied up capital. Their profits are flat to falling, and they trade at 5-12x earnings.",
  positioning="SRM is growing 94% while its peers shrink because it works in a less crowded niche: hill roads, tunnels and slope stabilisation for NHIDCL, BRO and state agencies, where fewer bidders qualify. It is now taking that execution record into national packages (Nashik Ring Road).",
  gap="SRM trades at 7.7x TTM profit against a peer median near 10x, despite far faster growth and a higher ROCE (32% vs 8-18%). The market applies the road-EPC sector discount to it, and adds a further discount for small size, a 2024 listing with a thin float (72.6% promoter), a negative FY25 CFO and lumpy, order-driven revenue. The gap closes only if it converts profit to cash at scale.",
 ),
 "FRONTSP": dict(
  universe_peers=["TEXRAIL", "ORIRAIL", "PITTIENG", "KROSS", "AUTOAXLES"],
  external_peers=[
   dict(name="Jamna Auto Industries", pe=23.5, roce=27.0, mcap_cr=5483, growth="TTM revenue ~Rs 2,650 Cr; growth 16-32% (sources differ)", asof="6-Nov-2026", url="https://www.valueresearchonline.com/stocks/42752/jamna-auto-industries-ltd/"),
   dict(name="Gabriel India", pe=76.5, roce=26.4, mcap_cr=26902, growth="FY26 revenue Rs 4,667 Cr, +14.9%; EBITDA margin 9.7%", asof="3-Nov-2026", url="https://www.valueresearchonline.com/stocks/42117/gabriel-india-ltd/"),
  ],
  competitors="Railway-component peers (Texmaco, Oriental Rail, Pitti) grew sales 10-25% a year at 7-14% operating margins. Suspension leaders are larger and steadier: Jamna Auto at ~23x and Gabriel India (+15% FY26 revenue) at ~76x.",
  positioning="Frontier's 27% EBITDA margin is roughly double its rail peers'. It comes from RDSO-approved status in coil, forged and air springs, where approved vendors are few, and from early volume on Vande Bharat and LHB air springs. FY27 guidance (Rs 500 Cr revenue) implies ~55% growth.",
  gap="At ~26x TTM (28x FY26) it sits above rail-ancillary peers (~15-17x) but far below the suspension leaders. The premium over rail peers reflects its margin and growth; the discount to Jamna and Gabriel reflects dependence on one customer (Indian Railways), L1 tender pricing that can be competed away, a low promoter stake with little institutional ownership, and unverified CFO. The market is pricing it as a high-quality railway vendor, not an auto-suspension franchise.",
 ),
 "GANDHITUBE": dict(
  universe_peers=["VENUSPIPES", "HITECH", "RATNAVEER", "JTLIND", "HARIOMPIPE"],
  external_peers=[
   dict(name="Ratnamani Metals & Tubes", pe=37.7, roce=20.0, mcap_cr=16322, growth="FY26 revenue ~Rs 4,616 Cr; EBITDA margin ~15-20%", asof="30-Oct-2026", url="https://www.valueresearchonline.com/stocks/44017/ratnamani-metals-tubes-ltd/"),
  ],
  competitors="Pipe and tube peers are growing faster (Venus 23%, Hi-Tech 27%, Ratnaveer 33% 3Y sales CAGR) on water, oil and gas, and infrastructure demand, but at 3-14% operating margins. Ratnamani, the stainless and specialty-tube leader, earns ~15-20% EBITDA and trades near 38x.",
  positioning="Gandhi earns a ~41% operating margin (ex other income) in a small precision niche: seamless and welded tubes for fuel-injection and hydraulic lines, plus nuts. Large mills ignore this niche and customers rarely switch qualified suppliers. It returns cash through dividends and a ~Rs 78 Cr buyback rather than chasing volume.",
  gap="It trades at ~14x against a peer median of ~29x and Ratnamani's ~38x, despite the best margins and ROCE in the group. Three reasons: growth is ~9-11% a year while peers grow 20-30%, and this pipe cycle rewards growth; the niche has no visible reinvestment runway; and part of PAT is treasury income, so the operating P/E is higher than the headline. It is priced as a cash-returning bond-like stock, not a compounder.",
 ),
 "GULPOLY": dict(
  universe_peers=["TRUALT", "GODAVARIB", "DHAMPURSUG", "UTTAMSUGAR", "AVADHSUGAR", "DALMIASUG", "MAGADSUGAR", "DWARKESH"],
  external_peers=[
   dict(name="Balrampur Chini Mills", pe=35.5, roce=13.9, mcap_cr=13418, growth="Integrated sugar + largest UP distillery", asof="6-Aug-2026", url="https://www.motilaloswal.com/share-market/peer-comparison/balrampur-chini-mills-ltd"),
   dict(name="Triveni Engineering", pe=18.4, roce=12.0, mcap_cr=5162, growth="Sugar, multi-feed distillery (#2 ethanol supplier), engineering", asof="6-Aug-2026", url="https://www.motilaloswal.com/share-market/peer-comparison/triveni-engineering-and-industries-ltd"),
  ],
  competitors="Sugar-ethanol peers have flat to falling 3Y sales and profit (Dhampur, Dwarikesh, Avadh, Magadh all show negative profit CAGRs) at 6-15% ROCE, yet trade at 12-24x. The large integrated players trade higher: Balrampur ~35x, Triveni ~18x.",
  positioning="Gulshan is one of the few grain-based ethanol pure plays with 810 KLPD now at full utilisation, so it is growing (+33% revenue, +332% FY26 profit) while cane-based peers are stuck. Grain distilleries can run all year, unlike seasonal cane molasses.",
  gap="Gulshan trades at ~6x TTM (9.5x FY26) against a peer median of ~17x, with double the ROCE. The market reads its earnings as a policy-set peak spread: ethanol prices are administered, grain feedstock (FCI rice, maize) is volatile, and once E20 is met allocations may be cut. Cane peers carry sugar, power and land assets that give them steadier earnings and a higher multiple. Near-zero institutional ownership (0.3%) and the recency of the earnings jump add to the discount.",
 ),
 "DYCL": dict(
  universe_peers=["UNIVCABLES", "PARACABLES", "VIDYAWIRES", "BIRLACABLE", "504240", "HPL"],
  external_peers=[
   dict(name="KEI Industries", pe=43.9, roce=20.2, mcap_cr=36787, growth="Revenue growth ~15-20%", asof="9-Oct-2026", url="https://www.valueresearchonline.com/stocks/42919/kei-industries-ltd/peer-comparison/"),
   dict(name="Polycab India", pe=43.4, roce=34.9, mcap_cr=None, growth="Revenue growth ~22-32%", asof="9-Oct-2026", url="https://www.valueresearchonline.com/stocks/249951/polycab-india-ltd/peer-comparison/"),
   dict(name="RR Kabel", pe=50.0, roce=28.4, mcap_cr=None, growth="Revenue growth ~20-38%", asof="9-Oct-2026", url="https://www.motilaloswal.com/share-market/peer-comparison/r-r-kabel-ltd"),
  ],
  competitors="The large cable makers (Polycab, KEI, RR Kabel) are growing 15-35% a year at 20-35% ROCE and trade at 43-50x, helped by branded retail wires and exports. Small B2B cable peers (Universal, Paramount, Delton, Birla Cable) trade at 11-28x.",
  positioning="Dynamic is a B2B power-cable and conductor maker for discoms, EPC contractors and railways, riding the RDSS distribution-upgrade programme. Its order book is ~Rs 829 Cr (about 8 months of revenue) and it posted 17% revenue and 30% profit growth in FY26.",
  gap="At ~19x it trades at a ~32% discount to the combined peer median (~27.5x) and at less than half the large-cap cable multiple, while sitting near the small B2B peers. The large players earn their premium with brands, retail distribution (B2C wires), export mix and pricing power; Dynamic sells through L1 tenders at ~10% margins and is exposed to the RDSS scheme's end date. Q4 margin pressure and withdrawn bank ratings (needs confirmation that debt was repaid) keep it at a discount. The gap is mostly justified by business mix, not mispricing.",
 ),
 "CRIZAC": dict(
  universe_peers=[],
  external_peers=[
   dict(name="IDP Education (ASX: IEL)", pe=None, roce=None, mcap_cr=None, growth="Share price ~A$2.1-2.3 vs 52-week high A$6.74; softer student volumes; trailing P/E unstable (14-90x+ on depressed earnings)", asof="Jul-2026", url="https://www.investsmart.com.au/security/asx/iel/idp-education-limited/financials"),
  ],
  competitors="The global listed comparable, IDP Education, has lost roughly two-thirds of its value as the UK, Canada and Australia tightened student visas, and its earnings have collapsed. There is no Indian listed peer; the rest of the industry (ApplyBoard, Adventus, many agent networks) is private.",
  positioning="Crizac is a B2B aggregator. Thousands of sub-agents route applications through its platform to UK universities, and it earns commission per enrolment. FY26 revenue grew 23% and profit 41%, so it has been taking share even as volumes softened, because universities are consolidating onto fewer, compliant aggregators.",
  gap="At ~12-13x earnings with ~60% FCF conversion it looks cheap for an asset-light platform. The market is pricing in an IDP-style policy shock: 97% of revenue is UK, Q1 FY27 revenue fell 4%, and promoters sold 20% in an all-OFS IPO. The discount is a rational policy-risk discount. It narrows only if destination diversification shows up in the numbers.",
 ),
 "JSLL": dict(
  universe_peers=["SHALBY", "INDRAMEDCO", "KMCSHIL", "UNIHEALTH", "GKSL"],
  external_peers=[
   dict(name="Narayana Hrudayalaya", pe=44.3, roce=None, mcap_cr=38080, growth="FY26 EBITDA margin 21.7% (India hospitals 25.1%)", asof="13-Nov-2026", url="https://www.valueresearchonline.com/stocks/108795/narayana-hrudayalaya-ltd/key-ratios/"),
   dict(name="Kovai Medical Center", pe=25.5, roce=None, mcap_cr=6004, growth="FY26 EBITDA margin ~27.6%", asof="older forum snapshot", url="https://stockanalysis.com/quote/nse/KOVAI/financials/"),
  ],
  competitors="Listed hospitals are growing 10-30% a year at 15-28% EBITDA margins and trade at 17-45x (Narayana ~44x; small hospital peers 17-64x). There is no sizeable listed Ayurveda hospital chain to compare against directly.",
  positioning="Jeena Sikho runs Ayurveda-and-Panchakarma hospitals (HiiMS) that need far less equipment capex per bed than allopathic hospitals, so it earns a 44% EBITDA margin and a 45% ROCE. It is the only scaled listed player in organised Ayurveda care.",
  gap="It trades at ~17x against hospital peers at ~31x (median) and Narayana at ~44x, despite twice their margin and much faster growth. The market discounts it because: the margin looks too good and part of revenue has been government-panel/scheme business; Ayurveda efficacy claims carry regulatory and reputational risk; FCF is ~23% of profit; and the profit jump (+178%) is very recent. The discount is mostly a credibility discount. Verifying revenue mix and cash conversion would show whether it is too large.",
 ),
 "544150": dict(
  universe_peers=["BAJEL", "PENIND", "MBEL", "EPACKPEB", "INTERARCH"],
  external_peers=[
   dict(name="Skipper Ltd", pe=29.5, roce=None, mcap_cr=6619, growth="Transmission towers, poles, pipes", asof="2-Oct-2026", url="https://www.tijorifinance.com/company/skipper-ltd/"),
   dict(name="KEC International", pe=21.5, roce=18.0, mcap_cr=12511, growth="Transmission EPC leader", asof="May-2026", url="https://www.tijorifinance.com/company/kec-international-limited/benchmarking"),
   dict(name="Kalpataru Projects", pe=20.7, roce=19.4, mcap_cr=None, growth="Transmission & infra EPC", asof="5-Oct-2026", url="https://www.valueresearchonline.com/stocks/42872/kalpataru-projects-international-ltd/peer-comparison/"),
  ],
  competitors="Transmission-tower and EPC leaders (Skipper, KEC, Kalpataru) trade at 21-30x on 16-19% ROCE as the national grid and renewables build-out drives order books. Fabrication peers in the universe (Pennar, M&B, EPack, Interarch) trade at 15-22x.",
  positioning="KP Green fabricates towers, solar module-mounting structures and substation steel. Its sister companies (KPI Green, KP Energy) give it a captive pipeline: revenue grew 79% to Rs 1,246 Cr in FY26 and the order book is ~Rs 1,831 Cr.",
  gap="At ~10x TTM (8x FY26) it trades at less than half its peers. The discount comes from: an SME listing (thin liquidity, not index-eligible); a large but unquantified share of revenue from related KP Group companies, which makes margins and receivables hard to trust; D/E of 1.35; and TTM profit already below FY26. Until the related-party share is disclosed and falls, the gap is a governance and quality discount, not a free lunch.",
 ),
 "APCOTEXIND": dict(
  universe_peers=["NOCIL", "STYRENIX", "BEPL", "ROSSARI", "TNPETRO"],
  external_peers=[],
  competitors="Polymer and rubber-chemical peers are mixed. NOCIL has flat sales and falling profit (3.8% ROCE), Styrenix and Bhansali grow 6-17% at 17-23% ROCE, and the group trades at 6-29x.",
  positioning="Apcotex is one of India's few synthetic-latex and NBR producers, protected by anti-dumping duties on NBR. Profit nearly doubled in FY26 on flat revenue as margins recovered, and it is adding Rs 210 Cr of capacity.",
  gap="On TTM profit (which includes a very strong Q1 FY27) it trades at ~15x, close to the peer median; on audited FY26 profit it is ~25x, a premium. There is no large mismatch. The market prices it as a mid-cycle specialty-chemical name whose margin recovery depends on Chinese import pricing and duty protection.",
 ),
 "ARROWGREEN": dict(
  universe_peers=["POLYPLEX", "COSMOFIRST", "NAHARPOLY"],
  external_peers=[
   dict(name="Uflex", pe=6.9, roce=7.2, mcap_cr=4716, growth="Flexible packaging & films; sector median P/E ~19.5", asof="11-Sep-2026", url="https://www.valueresearchonline.com/stocks/44961/uflex-ltd/"),
  ],
  competitors="Commodity film makers (Polyplex, Cosmo First, Uflex) trade at 7-14x on 7-10% ROCE after a long BOPET/BOPP down-cycle.",
  positioning="Arrow is not a commodity film maker. It sells patented water-soluble and biodegradable films (Green, +52% in FY26) and security and anti-counterfeiting products (High-tech), with a 32% ROCE and no debt.",
  gap="It trades at ~14x TTM (~22x on audited FY26), a premium to film makers that its returns and patents justify. It is not priced as a specialty-materials compounder because FY26 revenue fell 18%, the security business is lumpy and government-dependent, and the Q1 FY27 rebound is unverified. The market is waiting for proof that Green can carry the company.",
 ),
 "SOTL": dict(
  universe_peers=["PANAMAPET", "GANDHAR", "VEEDOL"],
  external_peers=[
   dict(name="Castrol India", pe=19.2, roce=60.3, mcap_cr=19441, growth="Lubricant brand leader; dividend yield ~4.5%", asof="3-Nov-2026", url="https://www.valueresearchonline.com/stocks/41510/castrol-india-ltd/peer-comparison/"),
   dict(name="Gulf Oil Lubricants", pe=12.2, roce=None, mcap_cr=5259, growth="Lubricant brand; dividend yield ~4.8%", asof="3-Nov-2026", url="https://www.valueresearchonline.com/stocks/41510/castrol-india-ltd/peer-comparison/"),
  ],
  competitors="Specialty-oil peers Panama Petrochem and Gandhar also show inflated TTM profits (P/E 4-6x), so the base-oil windfall is industry-wide. Branded lubricant leaders trade at 12-19x with 4-5% dividend yields.",
  positioning="Savita is India's leading transformer-oil supplier, which ties it to the grid and transformer build-out, and it has a smaller Savsol lubricant brand.",
  gap="On TTM profit it looks as cheap as its specialty-oil peers (~8x), but that is the same windfall. On normalised FY26 profit it is ~24.5x, above Gulf Oil and around Castrol, which earn far higher ROCE with stronger brands. The market prices the whole group off the windfall and also discounts the pending merger with a promoter entity. On a normalised basis, Savita is not cheap relative to peers.",
 ),
 "TAC": dict(
  universe_peers=["NPST", "CAPILLARY", "SUBEXLTD", "NUCLEUS", "QUICKHEAL"],
  external_peers=[
   dict(name="Tenable (US)", pe=None, roce=None, mcap_cr=None, growth="Revenue ~+10%; forward EV/sales ~3.9x; forward P/E ~11-16x", asof="Aug-2026", url="https://stockanalysis.com/stocks/TENB/statistics/"),
   dict(name="Qualys (US)", pe=17.5, roce=None, mcap_cr=None, growth="Revenue ~+10%; P/S ~8x; EV/EBITDA ~13.5x", asof="Aug-2026", url="https://brimindinvest.com/compare/tenb-vs-qlys"),
  ],
  competitors="The global vulnerability-management leaders are growing ~10% a year and trade at 4-8x sales and ~11-19x forward earnings. Indian listed software peers range from loss-making (Quick Heal) to high-growth fintech/SaaS at 60-73x (NPST, Capillary).",
  positioning="TAC sells risk-quantification and vulnerability-management software (ESOF) through partners. FY26 revenue grew 88% and EBITDA margin was 54%, from a very small base (Rs 57 Cr).",
  gap="At ~34x earnings and ~13x sales it trades well above the global leaders but below Indian high-growth SaaS. The premium over Tenable and Qualys is for growth, but that growth is lumpy and partner-driven (H2 profit fell 31%), and there is no disclosed ARR or retention. The market prices it like Indian SaaS while its revenue quality looks like project sales. The premium is the risk, not the opportunity.",
 ),
 "544406": dict(
  universe_peers=["DSSL", "ADSL", "SILVERTUC", "IVALUE", "ORIENTTECH"],
  external_peers=[],
  competitors="Indian IT-infrastructure integrators (Dynacons, iValue, Allied Digital, Silver Touch) grow 15-27% and trade at 13-47x, with Dynacons the closest comparable at ~15x and a 32% ROCE.",
  positioning="Unified Data-Tech runs IT-infrastructure integration plus AMC services for banks and enterprises, with a 35% ROCE and no debt. Revenue grew 31% in FY26, but profit grew only 19%.",
  gap="At ~17x it sits at the peer median, so there is no real mismatch. An SME discount (liquidity) is offset by its high ROCE. The planned diversification into unrelated safety equipment is the reason not to expect a re-rating.",
 ),
 "KRISHNADEF": dict(
  universe_peers=["TANAA", "AVANTEL", "PREMEXPLN", "IDEAFORGE"],
  external_peers=[
   dict(name="Garden Reach Shipbuilders", pe=31.6, roce=43.7, mcap_cr=25266, growth="Warship builder; industry P/E ~32", asof="29-Sep-2026", url="https://www.valueresearchonline.com/stocks/238018/garden-reach-shipbuilders-engineers-ltd/"),
   dict(name="Mishra Dhatu Nigam", pe=55.8, roce=None, mcap_cr=7436, growth="Defence special alloys; one analyst flags 50%+ overvaluation", asof="Jul-2026", url="https://www.stockezee.com/compare/grse-vs-midhani"),
  ],
  competitors="Defence names trade on a sector premium: GRSE ~32x with a 44% ROCE, MIDHANI ~56-74x, and small-cap defence names in the universe at 34x to over 100x, often on thin earnings.",
  positioning="Krishna supplies DMR-grade special steel and fabricated items to naval shipyards. It has qualified-vendor status, a 21% EBITDA margin and 30% growth, but a Rs 103 Cr order book (0.4x revenue).",
  gap="At ~36x TTM (47x FY26) it sits close to GRSE and below MIDHANI, so it is priced fully in line with the defence theme. There is no undervaluation versus peers. The risk is the reverse: it carries the sector premium while its order book is thinner than a shipbuilder's, so a theme de-rating would hit it harder.",
 ),
 "MODISONLTD": dict(
  universe_peers=["SALZERELEC", "HPL", "SHILCTECH", "INDOTECH"],
  external_peers=[],
  competitors="Electrical-equipment small caps (Salzer, HPL, Shilchar, Indo Tech) are growing 17-30% on the transmission and distribution capex cycle and trade at 18-31x.",
  positioning="Modison is a specialist in silver-based electrical contacts that sit inside every switchgear breaker. OEM qualification makes it sticky, and it rides the same T&D cycle.",
  gap="It trades at ~10x TTM and ~16x normalised FY26 profit against a peer median near 24x. The market refuses to capitalise silver-price gains: much of FY26 and Q1 FY27 profit came from inventory and hedge gains that reverse if silver falls. On ex-silver earnings (not disclosed) the true multiple is higher, so most of the apparent discount is an earnings-quality adjustment the market is already making.",
 ),
}
