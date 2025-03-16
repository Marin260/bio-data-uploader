package handlers

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/go-chi/chi"
)

func MountHealthRoutes(r *chi.Mux) {
	healthRouter := chi.NewRouter()

	healthRouter.Get("/ping", HelloWorldHandler)

	r.Mount("/health", healthRouter)
}

func HelloWorldHandler(w http.ResponseWriter, r *http.Request) {
	resp := make(map[string]string)
	resp["message"] = "Hello World"

	jsonResp, err := json.Marshal(resp)
	if err != nil {
		log.Fatalf("error handling JSON marshal. Err: %v", err)
	}

	_, _ = w.Write(jsonResp)
}
