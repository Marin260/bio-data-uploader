package handlers

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/exec"
	"strings"

	"github.com/go-chi/chi"
)

type ScriptInput struct {
	FilePath  string `json:"file_path"`
	FileName  string `json:"file_name"`
	StartDate string `json:"start_date"`
	EndDate   string `json:"end_date"`
}

const outputPath = "./output/"

func MountFileUploadRoutes(r *chi.Mux) {
	fileRouter := chi.NewRouter()

	fileRouter.Post("/upload", FileUploadHandler)

	r.Mount("/file", fileRouter)
}

func FileUploadHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("file-upload-controller::FileUpload() - Enter")

	// Get file from form
	log.Println("file-upload-controller::FileUpload() - Reading the request")

	resp := make(map[string]string)

	file, handler, err := r.FormFile("file")
	if err != nil {
		resp["error"] = fmt.Sprintf("Error while getting the file from the submited form - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}
	defer file.Close()

	// Check if the file is to big
	if handler.Size > 3000000 {
		resp["error"] = "File size to big"
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	// Create new local file
	log.Println("file-upload-controller::FileUpload() - Creating a new file")
	fileName := strings.TrimSuffix(handler.Filename, ".txt")
	dstFile, err := os.Create(outputPath + fileName + ".csv")
	if err != nil {
		resp["error"] = fmt.Sprintf("Error while creating a local file - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	// Copy form file into new file
	log.Println("file-upload-controller::FileUpload() - Copying request file content to the newly created file")
	_, err = io.Copy(dstFile, file)
	if err != nil {
		resp["error"] = fmt.Sprintf("Error while copying file content - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	// Prepare json input for the py script
	log.Println("file-upload-controller::FileUpload() - Creating json input")
	startDate := r.Form.Get("start") //c.Request.FormValue("start")
	endDate := r.Form.Get("end")
	scriptInputJSON := ScriptInput{FilePath: outputPath + fileName + ".csv", FileName: fileName, StartDate: startDate, EndDate: endDate}
	scriptInputFile, err := os.Create(outputPath + fileName + ".json")
	if err != nil {
		resp["error"] = fmt.Sprintf("Error while creating a local file - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	encoder := json.NewEncoder(scriptInputFile)
	err = encoder.Encode(scriptInputJSON)
	if err != nil {
		resp["error"] = fmt.Sprintf("Error while encoding json - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	// Run python script
	log.Println("file-upload-controller::FileUpload() - Running Python script")
	out, err := exec.Command("python3", "./py/sleep_analysis.py", "-fn", fileName+".json").CombinedOutput()
	if err != nil {
		fmt.Println(string(out))
		fmt.Println(err)
		resp["error"] = fmt.Sprintf("Error while runinng the script - %s", err)
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("error handling JSON marshal. Err: %v", err)
		}
		w.Write(jsonResp)
		return
	}

	w.Header().Set("Content-Type", "application/json")

	resp["fileName"] = fileName
	jsonResp, err := json.Marshal(resp)
	if err != nil {
		log.Fatalf("error handling JSON marshal. Err: %v", err)
	}
	w.Write(jsonResp)

	// Removing all the created files
	defer removeFiles(fileName, scriptInputFile, dstFile)
	fmt.Println(fileName)

	log.Println("file-upload-controller::FileUpload() - Exit")
}

func removeFiles(fileName string, jsonFile *os.File, csvFile *os.File) {
	log.Println("file-upload-controller::removeFiles() - Enter")

	jsonFile.Close()
	csvFile.Close()

	log.Println("file-upload-controller::removeFiles() - Removing files")
	err := os.Remove(outputPath + fileName + ".json")
	if err != nil {
		log.Println("file-upload-controller::removeFiles() - Error while removing files:", err)
	}
	err = os.Remove(outputPath + fileName + ".csv")
	if err != nil {
		log.Println("file-upload-controller::removeFiles() - Error while removing files:", err)
	}

	log.Println("file-upload-controller::removeFiles() - Exit")
}

func FileZipHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("file-controller::Zip() - Enter")
	//go filePath := fmt.Sprintf("./output/%s.zip", c.Params.ByName("name"))

	log.Println("file-controller::Zip() - Exit")
}
