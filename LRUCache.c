#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include "lru.h"

//Defining a node structure
typedef struct lru_node {
    char *key;
    void *item;
    struct lru_node *prev;
    struct lru_node *next;
} lruNode;
//Defining a lru cache structure
typedef struct lru_cache {
    int capacity;
    int size;
    lruNode *head;
    lruNode *tail;
} lru_t;



/* Create a new (empty) lru; return NULL if error. */
lru_t *lru_new(const int capacity) {
    //Allocating memory for a new cache
    lru_t *cache = (lru_t *)malloc(sizeof(lru_t));
    //Checks for NULL caches (Error)
    if (cache == NULL) {
        return NULL; // Return NULL if error
    }
    //Initializing the cache attributes
    cache->capacity = capacity;
    cache->size = 0;
    cache->head = NULL;
    cache->tail = NULL;
    return cache;
}

bool lru_insert(lru_t *ht, const char *key, void *item) {
    //Returns false if any parameter is NULL as instructed
    if (ht == NULL || key == NULL || item == NULL) {
        return false;
    }

    //Iterating through the lru to see if there is a duplicate key 
    lruNode *current = ht->head;
    while (current != NULL) {
        //Check if the key already exists, and returns false if it does
        if (strcmp(current->key, key) == 0) {
            return false;
        }
        current = current->next;
    }

    //If the key doesn't exist; it inserts a new node at the front
    lruNode *newNode = (lruNode *)malloc(sizeof(lruNode));
    //Returns false if memory allocation fails
    if (newNode == NULL) {
        return false;
    }
    //Copying the key string
    newNode->key = strdup(key);
    newNode->item = item;

    newNode->prev = NULL;
    newNode->next = ht->head;
    if (ht->head != NULL) {
        ht->head->prev = newNode;
    } else {
        ht->tail = newNode;
    }
    ht->head = newNode;

    //Increases the size of the LRU cache when something is inserted
    ht->size++;

    //This right here checks the capacity and if its full, it removes the Least Used Item
    if (ht->size > ht->capacity) {
        lruNode *tail = ht->tail;
        ht->tail = tail->prev;
        if (ht->tail != NULL) {
            ht->tail->next = NULL;
        } else {
            //Emptying out the Cache
            ht->head = NULL;
        }
        //Freeing the old allocated memory
        free(tail->key);
        free(tail);
        //Decreases the size of the cache
        ht->size--;
    }
    //If everything is done correctly
    return true;
}

void *lru_find(lru_t *cache, const char *key) {
    if (cache == NULL || key == NULL) {
        //Returns NULL if key is not found or cache is null as instructed
        return NULL;
    }
    //Beggining the iteration process to search for given input
    lruNode *current = cache->head;
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            //If the key matches, it moves the node to the front
            if (current != cache->head) {
                //Moving the node to the front of the list
                current->prev->next = current->next;
                if (current->next != NULL) {
                    current->next->prev = current->prev;
                } else {
                    cache->tail = current->prev;
                }


                current->next = cache->head;
                current->prev = NULL;

                if (cache->head != NULL) {
                    cache->head->prev = current;
                }

                cache->head = current;
            }
            //Returning the Item associated with the key
            return current->item;
        }
        current = current->next;
    }

   //This line was used for Debugging: printf("Key %s not found\n", key);
   // Returns null if key is not found
    return NULL;
}

void lru_print(lru_t *ht, FILE *fp, void (*itemprint)(FILE *fp, const char *key, void *item)) {
    if (fp == NULL) {
        //Ignore if NULL fp
        return;
    }

    if (ht == NULL) {
        //Printing (null) if null ht
        printf("(null)");
        return;
    }

    if (itemprint == NULL) {
        fprintf(fp, "Table with no items\n");
        return; //Prints a table with no items if NULL itemprint
    }

    lruNode *current = ht->head;
    while (current != NULL) {
        //Prints (null) if the item associated with the key is NULL
        if (current->item == NULL) {
            fprintf(fp, "(null)\n");
        } else {
            //Calls the itemprint function to print out the items
            itemprint(fp, current->key, current->item);
        }
        //Iterating through
        current = current->next;
    }
}
void lru_iterate(lru_t *ht, void *arg, void (*itemfunc)(void *arg, const char *key, void *item)) {
    if (ht == NULL || itemfunc == NULL) {
        //Do nothing if ht or itemfunc is null
        return;
    }
    //Setting up the iteration process
    lruNode *current = ht->head;
    while (current != NULL) {
        //Call the itemfunc function on each item, until the end of the lru
        itemfunc(arg, current->key, current->item);
        current = current->next;
    }
}
void lru_delete(lru_t *ht, void (*itemdelete)(void *item)) {
    if (ht == NULL) {
        return; //Ignores null ht
    }

    lruNode *current = ht->head;
    while (current != NULL) {
        //Traversing the cache to check if item is deletable
        lruNode *temp = current;
        current = current->next;

        if (itemdelete != NULL && temp->item != NULL) {
            //Calls itemdelete function on each item if not null
            itemdelete(temp->item);
        }
        //Deallocating the memory
        free(temp->key);
        free(temp);
    }
    //Resetting it for future use
    ht->head = NULL;
    ht->tail = NULL;
    ht->size = 0;
}

