FROM gcc:10
WORKDIR /app/
COPY ./* ./
RUN g++ comp.cpp -o program
RUN chmod +x program