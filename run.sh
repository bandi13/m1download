rm Activity-* M1Tx.csv -f && \
    python3 loadM1.py && \
    libreoffice M1Tx.csv
