flowchart TD

subgraph group_interface["Interface &amp; Configuration"]
  node_cli["CLI Entry<br/>[__main__.py]"]
  node_options["Option Parser<br/>[options.py]"]
  node_engine["Download Engine<br/>[YoutubeDL.py]"]
end

subgraph group_extraction["Extraction &amp; Selection"]
  node_extractor_registry["Extractor Registry<br/>[__init__.py]"]
  node_site_extractors["Site Extractors"]
  node_search_extractors["Search Extractors<br/>[_search.py]"]
  node_google_search["Google Search<br/>[googlesearch.py]"]
  node_format_selection["Format Selection<br/>[YoutubeDL.py]"]
end

subgraph group_transfer["Network &amp; Transfer"]
  node_networking["Network Requests<br/>[common.py]"]
  node_cookies["Cookie Handling<br/>[cookies.py]"]
  node_cache[("Persistent Cache<br/>[cache.py]")]
  node_download_core["Download Core<br/>[common.py]"]
  node_protocol_downloaders["Protocol Downloaders"]
  node_fragment_download["Fragment Download<br/>[fragment.py]"]
end

subgraph group_processing["Processing &amp; Output"]
  node_metadata_parser["Metadata Parser<br/>[metadataparser.py]"]
  node_postprocessors["Postprocessors"]
  node_output_files["Downloaded Files"]
end

node_user(("User"))
node_ffmpeg{{"FFmpeg"}}
node_video_sites{{"Media Websites"}}
node_search_sites{{"Search Websites"}}

node_user -->|"invokes"| node_cli
node_cli -->|"parses options"| node_options
node_cli -->|"starts engine"| node_engine
node_engine -->|"dispatches"| node_extractor_registry
node_extractor_registry -->|"selects extractor"| node_site_extractors
node_site_extractors -->|"requests pages"| node_networking
node_site_extractors -->|"returns metadata"| node_engine
node_search_extractors -->|"fetches results"| node_networking
node_search_extractors -->|"returns URLs"| node_engine
node_google_search -->|"fetches results"| node_networking
node_networking -->|"fetches media data"| node_video_sites
node_networking -->|"fetches search pages"| node_search_sites
node_engine -->|"selects formats"| node_format_selection
node_engine -->|"loads cookies"| node_cookies
node_engine -->|"reads cache"| node_cache
node_engine -->|"downloads formats"| node_download_core
node_download_core -->|"selects protocol"| node_protocol_downloaders
node_download_core -->|"downloads fragments"| node_fragment_download
node_fragment_download -->|"requests fragments"| node_networking
node_fragment_download -->|"stores progress"| node_cache
node_engine -->|"runs processing"| node_postprocessors
node_engine -->|"applies metadata"| node_metadata_parser
node_download_core -->|"writes media"| node_output_files
node_postprocessors -->|"updates files"| node_output_files
node_postprocessors -.->|"invokes tool"| node_ffmpeg

click node_cli "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/__main__.py"
click node_options "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/options.py"
click node_engine "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py"
click node_extractor_registry "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/__init__.py"
click node_site_extractors "https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/extractor"
click node_search_extractors "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/youtube/_search.py"
click node_google_search "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/extractor/googlesearch.py"
click node_format_selection "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py"
click node_networking "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/networking/common.py"
click node_cookies "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/cookies.py"
click node_cache "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/cache.py"
click node_download_core "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/downloader/common.py"
click node_protocol_downloaders "https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/downloader"
click node_fragment_download "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/downloader/fragment.py"
click node_metadata_parser "https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/postprocessor/metadataparser.py"
click node_postprocessors "https://github.com/yt-dlp/yt-dlp/tree/master/yt_dlp/postprocessor"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_cli,node_options,node_engine,node_user toneBlue
class node_extractor_registry,node_site_extractors,node_search_extractors,node_google_search,node_format_selection toneAmber
class node_networking,node_cookies,node_cache,node_download_core,node_protocol_downloaders,node_fragment_download toneMint
class node_metadata_parser,node_postprocessors,node_output_files toneRose
class node_ffmpeg,node_video_sites,node_search_sites toneIndigo