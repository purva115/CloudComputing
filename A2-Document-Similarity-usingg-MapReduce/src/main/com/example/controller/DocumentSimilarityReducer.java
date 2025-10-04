package com.example.controller;

import java.io.IOException;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class DocumentSimilarityReducer extends Reducer<Text, Text, Text, Text> {
    
    private Text result = new Text();
    private DecimalFormat df = new DecimalFormat("#.##");
    private Map<String, Set<String>> documentWords = new HashMap<>();
    
    @Override
    public void reduce(Text key, Iterable<Text> values, Context context)
            throws IOException, InterruptedException {
        
        Set<String> allWords = new HashSet<>();
        
        // Combine all word sets for this document
        for (Text value : values) {
            String[] words = value.toString().split(",");
            for (String word : words) {
                if (!word.trim().isEmpty()) {
                    allWords.add(word.trim());
                }
            }
        }
        
        // Store document words for similarity calculation
        documentWords.put(key.toString(), allWords);
    }
    
    @Override
    protected void cleanup(Context context) throws IOException, InterruptedException {
        // Generate all pairs and calculate similarity
        List<String> docIds = new ArrayList<>(documentWords.keySet());
        
        for (int i = 0; i < docIds.size(); i++) {
            for (int j = i + 1; j < docIds.size(); j++) {
                String doc1 = docIds.get(i);
                String doc2 = docIds.get(j);
                
                Set<String> set1 = documentWords.get(doc1);
                Set<String> set2 = documentWords.get(doc2);
                
                double similarity = calculateJaccardSimilarity(set1, set2);
                
                // Format the output
                String similarityStr = df.format(similarity);
                if (similarityStr.equals("0")) {
                    similarityStr = "0.00";
                } else if (similarityStr.equals("1")) {
                    similarityStr = "1.00";
                } else if (!similarityStr.contains(".")) {
                    similarityStr += ".00";
                } else if (similarityStr.split("\\.")[1].length() == 1) {
                    similarityStr += "0";
                }
                
                Text pairKey = new Text(doc1 + ", " + doc2);
                result.set("Similarity: " + similarityStr);
                context.write(pairKey, result);
            }
        }
    }
    
    private double calculateJaccardSimilarity(Set<String> set1, Set<String> set2) {
        if (set1.isEmpty() && set2.isEmpty()) {
            return 1.0;
        }
        
        // Calculate intersection
        Set<String> intersection = new HashSet<>(set1);
        intersection.retainAll(set2);
        
        // Calculate union
        Set<String> union = new HashSet<>(set1);
        union.addAll(set2);
        
        return (double) intersection.size() / union.size();
    }
}