#include "AVLTree.h"
#include <iostream>

using namespace std;
//Constructor and destructor to manage memory
AVLTree::AVLTree() : root(NULL) {}
AVLTree::~AVLTree() {
  clear();
}


void AVLTree::clear(Node* node) {
  if (node) {
    clear(node->left);
    clear(node->right);
    delete node;
  }
}
int AVLTree::rangeQuery(const std::string &low, const std::string &high) {
  return countRange(root, low, high);
}

// Function gets height of the tree
int AVLTree::getHeight(Node *node) {
  if (node == nullptr) {
    return 0;
  }
  return node->height;
}

int getMax(int a, int b) {
  // Gets the maximum of two integers
  return (a > b) ? a : b;
}

Node* AVLTree::createNode(const string& value) {
  return new Node(value);
}

Node* AVLTree::insert(Node* node, const std::string &key) {
   if (node == nullptr) {
    if (root == nullptr) {
      root = createNode(key);
      return root;
    }
    else {
      return createNode(key);
    }
   }
   if (key < node->key) {
     node->left = insert(node->left, key);
   }
   else if (key > node->key) {
     node->right = insert(node->right, key);
   }
   else {
     return node;
   }
   node->height = 1 + getMax(getHeight(node->left), getHeight(node->right));
   // Balance the tree

   int balance = getBalance(node);
