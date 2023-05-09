package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type RequestForm struct {
	ID              int    `json:"id"`
	RequestMethod  string `json:"request_method"`
	RequestEndpoint string `json:"request_endpoint"`
	RequestHeaders  string `json:"request_headers"`
	RequestBody     string `json:"request_body"`
}

func main() {
	// Connect to the database
	db, err := sql.Open("mysql", "user:password@tcp(host:port)/dbname")
	if err != nil {
		log.Fatalf("Error opening database: %v", err)
	}
	defer db.Close()

	// Start the worker pool
	poolSize := 5
	requests := make(chan *http.Request, 10)
	var wg sync.WaitGroup
	for i := 0; i < poolSize; i++ {
		wg.Add(1)
		go worker(i, db, requests, &wg)
	}

	// Handle incoming requests
	http.HandleFunc("/execute", func(w http.ResponseWriter, r *http.Request) {
		// Get the request form from the database
		formID := r.FormValue("form_id")
		form, err := getRequestForm(db, formID)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error getting request form: %v", err), http.StatusInternalServerError)
			return
		}

		// Create the new request
		req, err := http.NewRequest(form.RequestMethod, form.RequestEndpoint, nil)
		if err != nil {
			http.Error(w, fmt.Sprintf("Error creating request: %v", err), http.StatusInternalServerError)
			return
			}

		// Add the headers to the request
		if form.RequestHeaders != "" {
			var headers map[string]string
			if err := json.Unmarshal([]byte(form.RequestHeaders), &headers); err != nil {
				http.Error(w, fmt.Sprintf("Error parsing headers: %v", err), http.StatusInternalServerError)
				return
			}
			for key, value := range headers {
				req.Header.Set(key, value)
			}
		}

		// Add the request body to the request
		if form.RequestBody != "" {
			reqBody := []byte(form.RequestBody)
			req.Body = ioutil.NopCloser(bytes.NewBuffer(reqBody))
			req.Header.Set("Content-Type", "application/json")
		}

		// Add any query parameters from the incoming request to the new request
		q := req.URL.Query()
		for key, values := range r.URL.Query() {
			for _, value := range values {
				q.Add(key, value)
			}
		}
		req.URL.RawQuery = q.Encode()

		// Add the new request to the worker pool
		requests <- req

		fmt.Fprint(w, "Request queued for execution.")
	})

	// Start the server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("Listening on port %s...\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

func getRequestForm(db *sql.DB, formID string) (*RequestForm, error) {
	var form RequestForm
	err := db.QueryRow("SELECT id, request_method, request_endpoint, request_headers, request_body FROM request_forms WHERE id = ?", formID).Scan(&form.ID, &form.RequestMethod, &form.RequestEndpoint, &form.RequestHeaders, &form.RequestBody)
	if err != nil {
	
