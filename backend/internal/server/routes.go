package server

import (
	"net/http"

	"example.com/packages/internal/api/handlers"
	"github.com/go-chi/chi"
	"github.com/go-chi/chi/middleware"
)

func (s *Server) RegisterRoutes() http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.Logger)

	handlers.MountHealthRoutes(r)
	handlers.MountFileUploadRoutes(r)
	//authhandler.MountAuthRoutes(r)
	//healthhandlers.MountHealthRoutes(r)

	return r
}
