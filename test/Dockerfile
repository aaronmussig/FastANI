FROM python:3.6-slim-buster

# Install OS requirements
RUN apt update -y -m && \
    DEBIAN_FRONTEND=noninteractive \
    apt install --no-install-recommends --no-install-suggests -y \
        wget \
        libpq-dev \
        libgomp1 \
        unzip \
        gcc \
        build-essential && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# Download required files
WORKDIR /tmp
RUN wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.33/fastANI-Linux64-v1.33.zip" && \
    unzip -o fastANI-Linux64-v1.33.zip && \
    mv fastANI /bin/fastANI_1.33 && \
    chmod +x /bin/fastANI_1.33 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.32/fastANI-Linux64-v1.32.zip" && \
    unzip -o fastANI-Linux64-v1.32.zip && \
    mv fastANI /bin/fastANI_1.32 && \
    chmod +x /bin/fastANI_1.32 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.31/fastANI-Linux64-v1.31.zip" && \
    unzip -o fastANI-Linux64-v1.31.zip && \
    mv fastANI /bin/fastANI_1.31 && \
    chmod +x /bin/fastANI_1.31 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.3/fastANI-Linux64-v1.3.zip" && \
    unzip -o fastANI-Linux64-v1.3.zip && \
    mv fastANI /bin/fastANI_1.3 && \
    chmod +x /bin/fastANI_1.3 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.2/fastANI-Linux64-v1.2.zip" && \
    unzip -o fastANI-Linux64-v1.2.zip && \
    mv fastANI /bin/fastANI_1.2 && \
    chmod +x /bin/fastANI_1.2 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.1/fastani-Linux64-v1.1.zip" && \
    unzip -o fastani-Linux64-v1.1.zip && \
    mv fastANI /bin/fastANI_1.1 && \
    chmod +x /bin/fastANI_1.1 && \
    wget "https://github.com/ParBLiSS/FastANI/releases/download/v1.0/fastani-Linux64-v1.0.zip" && \
    unzip -o fastani-Linux64-v1.0.zip && \
    mv fastani-Linux64-v1.0/fastANI /bin/fastANI_1.0 && \
    chmod +x /bin/fastANI_1.0 && \
    rm -rf /tmp/*

# Download genomes
RUN mkdir -p /genomes

WORKDIR /genomes

RUN wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/873/845/GCA_001873845.1_ASM187384v1/GCA_001873845.1_ASM187384v1_genomic.fna.gz" && \
    wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/783/845/GCA_002783845.1_ASM278384v1/GCA_002783845.1_ASM278384v1_genomic.fna.gz" && \
    wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/789/105/GCA_002789105.1_ASM278910v1/GCA_002789105.1_ASM278910v1_genomic.fna.gz" && \
    wget "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/001/886/815/GCA_001886815.1_ASM188681v1/GCA_001886815.1_ASM188681v1_genomic.fna.gz" && \
    mv "GCA_001873845.1_ASM187384v1_genomic.fna.gz" "GCA_001873845.1.fna.gz" && \
    mv "GCA_002783845.1_ASM278384v1_genomic.fna.gz" "GCA_002783845.1.fna.gz" && \
    mv "GCA_002789105.1_ASM278910v1_genomic.fna.gz" "GCA_002789105.1.fna.gz" && \
    mv "GCA_001886815.1_ASM188681v1_genomic.fna.gz" "GCA_001886815.1.fna.gz"

