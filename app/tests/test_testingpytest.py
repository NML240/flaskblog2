import pytest

@pytest.fixture()
def my_fixture():
  print("Creating fixture")
  yield
  print("Destroying fixture")

def test_1(my_fixture):
  print("Running test 1")



def test_2(my_fixture):
  print("Running test 2")

def test_3(my_fixture):
  print("Running test 3")
