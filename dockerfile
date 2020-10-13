FROM gcc:10
WORKDIR /app/
COPY ./* ./
RUN gcc comp.cpp -o program
RUN chmod +x program